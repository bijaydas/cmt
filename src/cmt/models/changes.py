from pydantic import BaseModel


class File(BaseModel):
    status: str
    path: str


class ChangeSet(BaseModel):
    files: list[File]
    diff: str


class AnalysisResult(BaseModel):
    total_files: int
    added_files: int
    modified_files: int
    deleted_files: int
    renamed_files: int
