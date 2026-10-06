import logging

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from cmt.core.settings import settings

logger = logging.getLogger(__name__)


class OpenAIProvider:
    def __init__(self) -> None:
        self.config = settings.get()

    def create_agent(self, system_prompt=None):
        if not system_prompt:
            raise RuntimeWarning("System Prompt required")
        llm = ChatOpenAI(
            model=self.config.model,
            api_key=SecretStr(self.config.api_key),
            timeout=30,
        )
        return create_agent(
            model=llm,
            system_prompt=system_prompt,
        )
