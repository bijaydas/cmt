from abc import ABC, abstractmethod

from cmt.models.changes import AnalysisResult, StagedChangeSet
from cmt.models.suggestion import CommitSuggestion


class AIProvider(ABC):
    @abstractmethod
    def generate_commit_message(
        self,
        change_set: StagedChangeSet,
        analysis: AnalysisResult
    ) -> CommitSuggestion:
        pass