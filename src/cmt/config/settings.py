from configparser import ConfigParser
from pathlib import Path

from pydantic import BaseModel
from cmt.exceptions import ConfigurationError


class OpenAIConfig(BaseModel):
    api_key: str
    model: str


class Settings:
    CONFIG_DIR: Path = Path.home() / ".config" / "cmt"

    CONFIG_FILE: Path = CONFIG_DIR / "config.json"
    OPEN_AI_DEFAULT_MODEL: str = "gpt-4o-mini"

    def set(self, openai_config: OpenAIConfig):
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        config = ConfigParser()
        config["openai"] = {
            "api_key": openai_config.api_key,
            "model": openai_config.model
        }

        with open(self.CONFIG_FILE, "w") as f:
            config.write(f)

    def get(self) -> OpenAIConfig:
        if not self.CONFIG_FILE.exists():
            raise FileNotFoundError(
                "Configuration file not found. Run `cmt config set` to set it up."
            )

        config = ConfigParser()
        config.read(self.CONFIG_FILE)

        api_key = config["openai"].get("api_key")
        model = config["openai"].get("model")

        if not api_key:
            raise ConfigurationError(
                "API key not found in the configuration. Run `cmt config set` to set it up."
            )

        if not model:
            raise ConfigurationError(
                "Model not found in the configuration. Run `cmt config set` to set it up."
            )

        return OpenAIConfig(
            api_key=api_key,
            model=model
        )