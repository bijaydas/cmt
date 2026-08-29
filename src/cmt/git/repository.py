import subprocess
from pathlib import Path

from cmt.models.changes import StagedChangeSet, StagedFile


class Repository:
    def __init__(self, root: Path | None = None):
        self.root = Path(root) if root is not None else Path.cwd()

    def _execute(self, command: list[str]) -> subprocess.CompletedProcess:
        return subprocess.run(
            command,
            cwd=self.root,
            capture_output=True,
            check=True,
            text=True
        )

    def is_git_repository(self):
        try:
            result = self._execute(["git", "rev-parse", "--is-inside-work-tree"])
            return result.stdout.strip() == "true"
        except subprocess.CalledProcessError:
            return False

    def _get_staged_files(self) -> list[StagedFile]:
        result = self._execute(["git", "diff", "--name-status", "--cached"])

        files: list[StagedFile] = []

        for line in result.stdout.splitlines():
            _line = line.split("\t", 1)
            status, path = _line
            files.append(StagedFile(status=status, path=path))

        return files

    def _get_staged_diff(self) -> str:
        result = self._execute(["git", "diff", "--cached"])
        return result.stdout

    def get_staged_changes(self) -> StagedChangeSet:
        return StagedChangeSet(
            files=self._get_staged_files(),
            diff=self._get_staged_diff()
        )

    def commit(self, message: str) -> subprocess.CompletedProcess:
        return self._execute(["git", "commit", "-m", message])