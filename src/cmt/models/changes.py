from pydantic import BaseModel


class StagedFile(BaseModel):
    status: str
    path: str

class StagedChangeSet(BaseModel):
    files: list[StagedFile]
    diff: str

class AnalysisResult(BaseModel):
    total_files: int
    added_files: int
    modified_files: int
    deleted_files: int
    renamed_files: int