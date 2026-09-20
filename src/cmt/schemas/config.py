from pydantic import BaseModel


class AIConfig(BaseModel):
    api_key: str
    model: str
