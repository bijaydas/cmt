from abc import ABC, abstractmethod

from cmt.models.changes import AnalysisResult, ChangeSet
from cmt.models.suggestion import ChangeSummary, CommitSuggestion


class AIProvider(ABC):
    @abstractmethod
    def generate_commit_message(
        self, change_set: ChangeSet, analysis: AnalysisResult
    ) -> CommitSuggestion:
        pass

    @abstractmethod
    def generate_summary(self, change_set: ChangeSet, analysis: AnalysisResult) -> ChangeSummary:
        pass
