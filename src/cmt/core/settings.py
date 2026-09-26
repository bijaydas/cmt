from configparser import ConfigParser
from pathlib import Path

from cmt.exceptions import ConfigurationError
from cmt.schemas.config import AIConfig


class Settings:
    APP_NAME: str = "cmt-cli"
    CONFIG_DIR: Path = Path.home() / ".config" / "cmt"
    CACHE_DIR: Path = CONFIG_DIR / "cache"
    LOGS_DIR: Path = CONFIG_DIR / "logs"

    CONFIG_FILE: Path = CONFIG_DIR / "config.ini"
    OPEN_AI_DEFAULT_MODEL: str = "gpt-4o-mini"

    def set(self, openai_config: AIConfig):
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

    def get(self) -> AIConfig:
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

        return AIConfig(api_key=api_key, model=model)


settings = Settings()
