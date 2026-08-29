from configparser import ConfigParser
from pathlib import Path

from pydantic import BaseModel

from cmt.exceptions import ConfigurationError


class Config(BaseModel):
    api_key: str
    model: str


class Settings:
    CONFIG_DIR: Path = Path.home() / ".config" / "cmt"
    CACHE_DIR: Path = CONFIG_DIR / "cache"

    CONFIG_FILE: Path = CONFIG_DIR / "config.ini"
    OPEN_AI_DEFAULT_MODEL: str = "gpt-4o-mini"

    def set(self, openai_config: Config):
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        config = ConfigParser()

        if openai_config.api_key:
            config["openai"] = {}

            if openai_config.api_key:
                config["openai"]["api_key"] = openai_config.api_key

            if openai_config.model:
                config["openai"]["model"] = openai_config.model

        with open(self.CONFIG_FILE, "w") as f:
            config.write(f)

    def get(self) -> Config:
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

        return Config(api_key=api_key, model=model)
