from pydantic import BaseModel


class CommitSuggestion(BaseModel):
    message: str
    description: str