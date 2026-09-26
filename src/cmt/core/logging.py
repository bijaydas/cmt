import logging
from logging.handlers import RotatingFileHandler

from cmt.core.settings import settings


def setup_logging():
    settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(
        settings.LOGS_DIR / f"{settings.APP_NAME}.log", maxBytes=1024 * 1024, backupCount=9
    )

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[handler],
    )
