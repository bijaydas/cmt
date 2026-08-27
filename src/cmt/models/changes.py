from pydantic import BaseModel


class StagedFile(BaseModel):
    status: str
    path: str