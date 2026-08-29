from cmt.models.changes import AnalysisResult, StagedChangeSet


class Analyzer:
    def analyze(self, change_set: StagedChangeSet) -> AnalysisResult:
        added = 0
        modified = 0
        deleted = 0
        renamed = 0
        total = 0

        for file in change_set.files:
            total += 1
            if file.status == "A":
                added += 1
            elif file.status == "M":
                modified += 1
            elif file.status == "D":
                deleted += 1
            elif file.status == "R":
                renamed += 1

        return AnalysisResult(
            total_files=total,
            added_files=added,
            modified_files=modified,
            deleted_files=deleted,
            renamed_files=renamed,
        )
