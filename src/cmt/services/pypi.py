import logging

import httpx

from cmt.core import settings
from cmt.schemas.general import VersionInfo

logger = logging.getLogger(__name__)


class PyPIService:
    def __init__(self):
        self._base_url = "https://pypi.org/pypi"

    def _get_package_info(self) -> dict:
        url = f"{self._base_url}/{settings.APP_NAME}/json"
        response = httpx.get(url)

        logger.debug("Received response with status code: %s", response.status_code)
        response.raise_for_status()

        return response.json()

    def any_update(self, current_version: str) -> VersionInfo:
        latest_info = self._get_package_info()
        latest_version = latest_info["info"]["version"]

        logger.debug("Current version: %s, Latest version: %s", current_version, latest_version)

        return VersionInfo(
            current_version=current_version,
            latest_version=latest_version,
            updated_required=latest_version != current_version,
        )
