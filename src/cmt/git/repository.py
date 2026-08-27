import subprocess
from cmt.models.changes import StagedFile
from pathlib import Path


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

    def get_staged_files(self) -> list[StagedFile]:
        result = self._execute(["git", "diff", "--name-status", "--cached"])

        files: list[StagedFile] = []

        for line in result.stdout.splitlines():
            if not line.strip():
                continue

            status, path = line.split("\t", 1)
            files.append(StagedFile(status=status, path=path))

        return files
