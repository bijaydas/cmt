import logging

import typer

from cmt.ai.openai import OpenAIProvider
from cmt.commands.command import CommandService
from cmt.core.console import console
from cmt.prompts.summary import SUMMARY_SYSTEM_PROMPT
from cmt.services import Analyzer, PromptService, Repository

logger = logging.getLogger(__name__)


class SummaryCommand(CommandService):
    llm = None

    def __init__(self) -> None:
        super().__init__()
        self.llm = OpenAIProvider()
        self.agent = self.llm.create_agent(SUMMARY_SYSTEM_PROMPT)
        self.repository_service = Repository()
        self.analyzer_service = Analyzer()
        self.prompt_service = PromptService()

    def _get_prompt(self):
        with console.get_console().status("[brand]Analyzing changes...[/brand]", spinner="dots"):
            changes = self.repository_service.get_current_changes()

            if len(changes.files) == 0:
                logger.info("No changes detected.")
                console.print_info("No changes detected.")
                raise typer.Exit(code=0)

        analysis_result = self.analyzer_service.analyze(changes)
        return self.prompt_service.get_summary_prompt(changes, analysis_result)

    def _get_summary(self, prompt) -> str:
        with console.get_console().status("[brand]Preparing summary...[/brand]", spinner="dots"):
            response = self.agent.invoke(prompt)
            return response["messages"][-1].content

    def run(self) -> None:

        prompt = self._get_prompt()
        logger.info("Prompt: %s", prompt.to_string())

        logger.info("Checking cache if exist")
        from_cache = self.get_cache(prompt.to_string())

        if from_cache:
            logger.info("Response from cache: %s", from_cache)
            console.print(console.render_summary_panel(from_cache))
        else:
            summary = self._get_summary(prompt)
            self.set_cache(prompt.to_string(), summary)

            logger.info("Response from agent: %s", summary)
            console.print(console.render_summary_panel(summary))
