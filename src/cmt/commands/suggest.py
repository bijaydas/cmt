import logging

from cmt.ai.openai import OpenAIProvider
from cmt.commands.command import CommandService
from cmt.prompts.suggest import COMMIT_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class SuggestCommand(CommandService):
    def __init__(self) -> None:
        super().__init__()
        self.llm = OpenAIProvider()
        self.agent = self.llm.create_agent(COMMIT_SYSTEM_PROMPT)

    def run(self, prompt) -> str:
        logger.info("Prompt: %s", prompt.to_string())

        logger.info("Checking cache if exist")

        from_cache = self.get_cache(prompt.to_string())

        if from_cache:
            logger.info("Response from cache: %s", from_cache)
            return from_cache

        response = self.agent.invoke(prompt)
        content = response["messages"][-1].content

        self.set_cache(prompt.to_string(), content)

        logger.info("Response from agent: %s", content)

        return content
