from pydantic import BaseModel


class CurrentSummaryResponse(BaseModel):
    summary: str
