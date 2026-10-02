import logging

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from cmt.ai.cache import CommitMessageCache
from cmt.ai.prompt import COMMIT_PROMPT_TEMPLATE, COMMIT_SYSTEM_PROMPT
from cmt.ai.provider import AIProvider
from cmt.core.settings import settings
from cmt.models.changes import AnalysisResult, StagedChangeSet, StagedFile
from cmt.models.suggestion import CommitSuggestion

logger = logging.getLogger(__name__)


class OpenAIProvider(AIProvider):
    def __init__(self) -> None:
        self.config = settings.get()

    def _build_prompt(self, changes: StagedChangeSet, analysis: AnalysisResult):
        staged_files = self._process_files(changes.files)
        staged_diffs = changes.diff

        return COMMIT_PROMPT_TEMPLATE.invoke(
            {
                "total_files": len(changes.files),
                "added_files": analysis.added_files,
                "modified_files": analysis.modified_files,
                "deleted_files": analysis.deleted_files,
                "renamed_files": analysis.renamed_files,
                "staged_files": staged_files,
                "staged_diffs": staged_diffs,
            }
        )

    @staticmethod
    def _process_files(files: list[StagedFile]) -> str:
        output = ""
        for file in files:
            output += f"{file.status} {file.path}\n"

        return output.strip()

    def _invoke(self, prompt) -> CommitSuggestion:
        model = ChatOpenAI(
            model=self.config.model,
            api_key=SecretStr(self.config.api_key),
            timeout=30,
        )
        logger.info("Invoking %s model with prompt:\n%s", self.config.model, prompt.to_string())

        agent = create_agent(
            model=model,
            system_prompt=COMMIT_SYSTEM_PROMPT,
            response_format=CommitSuggestion,
        )

        result = agent.invoke(prompt)

        return result["structured_response"]

    def generate_commit_message(
        self, change_set: StagedChangeSet, analysis: AnalysisResult
    ) -> CommitSuggestion:
        prompt = self._build_prompt(change_set, analysis)

        cache = CommitMessageCache()
        cached_message = cache.get(change_set.diff, self.config.model)

        if cached_message:
            suggestion = CommitSuggestion(
                message=cached_message.message, description=cached_message.description
            )
            logger.info(
                "Returning cached commit suggestion for the following changes:\n\n%s\n\n"
                "Commit message: %s",
                change_set.diff,
                suggestion.message,
            )
            return suggestion

        suggestion = self._invoke(prompt)

        logger.info("Generated new commit suggestion.\n%s", suggestion)

        cache.set(change_set.diff, self.config.model, suggestion)
        logger.info("Cached new commit suggestion.")

        suggestion = CommitSuggestion(
            message=suggestion.message, description=suggestion.description
        )

        return suggestion

    @staticmethod
    def commit_command(commit_suggestion: CommitSuggestion) -> str:
        if not commit_suggestion.description:
            return commit_suggestion.message
        return f"{commit_suggestion.message} \n\n{commit_suggestion.description}"
