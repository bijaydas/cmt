import hashlib
from pathlib import Path
import json

from cmt.config.settings import Settings
from cmt.models.suggestion import CommitSuggestion


class CommitMessageCache:
    def __init__(self):
        self.cache_dir = Path(Settings().CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _key(diff: str, model: str) -> str:
        return hashlib.sha256(f"{diff}-{model}".encode()).hexdigest()

    def set(self, diff: str, model: str, commit: CommitSuggestion):
        key = CommitMessageCache._key(diff, model)
        cache_file = self.cache_dir / key
        cache_file.write_text(commit.model_dump_json())

    def get(self, diff: str, model: str) -> CommitSuggestion | None:
        key = CommitMessageCache._key(diff, model)
        cache_file = self.cache_dir / key
        if cache_file.exists():
            return CommitSuggestion(**json.loads(cache_file.read_text()))
        return None
