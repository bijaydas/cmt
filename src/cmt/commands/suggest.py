import logging

import typer

from cmt.ai.openai import OpenAIProvider
from cmt.commands.command import CommandService
from cmt.core.console import console
from cmt.exceptions import CmtError
from cmt.prompts.suggest import COMMIT_SYSTEM_PROMPT
from cmt.services import Analyzer, PromptService, Repository
from cmt.utils import edit_with_vim

logger = logging.getLogger(__name__)


class SuggestCommand(CommandService):
    llm = None

    def __init__(self) -> None:
        super().__init__()
        self.llm = OpenAIProvider()
        self.agent = self.llm.create_agent(COMMIT_SYSTEM_PROMPT)
        self.repository_service = Repository()
        self.analyzer_service = Analyzer()
        self.prompt_service = PromptService()

    def _get_prompt(self):
        if not self.repository_service.is_git_repository():
            logger.error("Not a git repository.")
            raise CmtError("Not a git repository.")

        staged_files = self.repository_service.get_staged_changes()

        if not staged_files.files:
            message = "No staged files found. Please stage your changes before running."
            logger.warning(message)
            console.print_warning(message)
            raise typer.Exit(code=0)

        with console.get_console().status(
            "[brand]Analyzing staged changes...[/brand]", spinner="dots"
        ):
            analysis_result = self.analyzer_service.analyze(staged_files)

        return self.prompt_service.get_commit_prompt(staged_files, analysis_result)

    def _get_commit_message(self, prompt) -> str:
        with console.get_console().status(
            "[brand]Generating commit message...[/brand]", spinner="dots"
        ):
            response = self.agent.invoke(prompt)
            return response["messages"][-1].content

    def _commit(self, message: str) -> None:
        logger.info("Committing with message:\n\n%s", message)
        result = self.repository_service.commit(message)

        logger.info("Commit result:\n\n%s", result.stdout)
        console.print_success("Code committed")

    def _confirm(self, commit: str) -> None:
        while True:
            action = (
                typer.prompt(
                    "Would you like to use this commit message? [y]es / [e]dit / [n]o",
                    default="y",
                )
                .strip()
                .lower()[0]
            )

            if action == "n":
                console.print_warning("Aborted.")
                break

            if action == "e":
                commit = edit_with_vim(commit)
                console.print_suggested_commit(commit)

            if action == "y":
                self._commit(commit)
                break

    def run(self) -> None:
        prompt = self._get_prompt()
        logger.info("Prompt: %s", prompt.to_string())

        logger.info("Checking cache if exist")
        commit = self.get_cache(prompt.to_string())

        if commit:
            logger.info("Response from cache: %s", commit)
        else:
            commit = self._get_commit_message(prompt)
            self.set_cache(prompt.to_string(), commit)
            logger.info("Response from agent: %s", commit)

        console.print_suggested_commit(commit)
        self._confirm(commit)
