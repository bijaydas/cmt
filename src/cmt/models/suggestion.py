from pydantic import BaseModel


class CommitSuggestion(BaseModel):
    message: str
    description: str


class ChangeSummary(BaseModel):
    summary: str
