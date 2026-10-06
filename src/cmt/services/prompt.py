from cmt.models.changes import AnalysisResult, ChangeSet, File
from cmt.prompts.suggest import COMMIT_PROMPT_TEMPLATE
from cmt.prompts.summary import SUMMARY_PROMPT_TEMPLATE


class PromptService:
    def __init__(self) -> None:
        pass

    def get_summary_prompt(self, change_set: ChangeSet, analysis: AnalysisResult):
        changed_files = self._stringify_files(change_set.files)

        prompt = SUMMARY_PROMPT_TEMPLATE.invoke(
            {
                "total_files": analysis.total_files,
                "added_files": analysis.added_files,
                "modified_files": analysis.modified_files,
                "deleted_files": analysis.deleted_files,
                "renamed_files": analysis.renamed_files,
                "changed_files": changed_files,
                "diffs": change_set.diff,
            }
        )
        return prompt

    def _stringify_files(self, files: list[File]) -> str:
        output = ""
        if len(files) == 0:
            return output

        for file in files:
            output += f"{file.status} {file.path}\n"

        return output.strip()

    def get_commit_prompt(self, change_set: ChangeSet, analysis: AnalysisResult):
        changed_files = self._stringify_files(change_set.files)

        prompt = COMMIT_PROMPT_TEMPLATE.invoke(
            {
                "total_files": analysis.total_files,
                "added_files": analysis.added_files,
                "modified_files": analysis.modified_files,
                "deleted_files": analysis.deleted_files,
                "renamed_files": analysis.renamed_files,
                "changed_files": changed_files,
                "diffs": change_set.diff,
            }
        )
        return prompt
