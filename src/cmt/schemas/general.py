from pydantic import BaseModel


class VersionInfo(BaseModel):
    current_version: str
    latest_version: str
    updated_required: bool
