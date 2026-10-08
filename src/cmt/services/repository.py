import logging
import subprocess
from pathlib import Path

from cmt.exceptions import GitError
from cmt.models.changes import ChangeSet, File

logger = logging.getLogger(__name__)


class Repository:
    def __init__(self, root: Path | None = None):
        self.root = Path(root) if root is not None else Path.cwd()

    def _execute(self, command: list[str]) -> subprocess.CompletedProcess:
        try:
            return subprocess.run(
                command, cwd=self.root, capture_output=True, check=True, text=True
            )
        except subprocess.CalledProcessError as e:
            output = "\n".join(filter(None, [e.stdout, e.stderr])).strip()
            output = output or "no error output was returned."
            raise GitError(output) from e

    def is_git_repository(self) -> bool:
        try:
            result = self._execute(["git", "rev-parse", "--is-inside-work-tree"])
            return result.stdout.strip() == "true"
        except GitError:
            return False

    def _get_staged_files(self) -> list[File]:
        result = self._execute(["git", "diff", "--name-status", "--cached"])

        files: list[File] = []

        for line in result.stdout.splitlines():
            _line = line.split("\t", 1)
            status, path = _line
            files.append(File(status=status, path=path))

        return files

    def _get_staged_diff(self) -> str:
        result = self._execute(["git", "diff", "--cached"])
        return result.stdout

    def get_staged_changes(self) -> ChangeSet:
        return ChangeSet(files=self._get_staged_files(), diff=self._get_staged_diff())

    def commit(self, message: str) -> subprocess.CompletedProcess:
        return self._execute(["git", "commit", "-m", message])

    def get_current_changes(self) -> ChangeSet:
        return ChangeSet(
            files=self._get_current_files(), diff=self._get_changes_for_non_deleted_files()
        )

    def _get_changes_for_non_deleted_files(self) -> str:

        if not self._check_if_any_commit_exits():
            return ""

        command = ["git", "diff", "HEAD", "--diff-filter=AM"]
        logger.info("Executing command: %s", " ".join(command))

        result = self._execute(command)
        logger.info("Command output: %s", result.stdout)

        return result.stdout

    def _get_current_files(self) -> list[File]:
        command = ["git", "diff", "HEAD", "--name-status"]
        is_zero_commits = not self._check_if_any_commit_exits()

        if is_zero_commits:
            command = ["git", "ls-files", "--others", "--exclude-standard"]

        logger.info("Executing command: %s", " ".join(command))
        result = self._execute(command)
        logger.info("Command output: %s", result.stdout)

        files: list[File] = []

        for line in result.stdout.splitlines():
            _line = line.split("\t", 1)
            _status = None
            _path = None

            if len(_line) > 1:
                _status, _path = _line
            else:
                _status = "A"
                _path = _line[0] if _line else ""

            files.append(File(status=_status, path=_path))

        return files

    def _check_if_any_commit_exits(self) -> bool:
        logger.info("Checking if any commit exists")
        try:
            result = self._execute(["git", "log", "-1"])
            return bool(result.stdout.strip())
        except GitError:
            return False
