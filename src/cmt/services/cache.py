import hashlib
import json
from pathlib import Path

from cmt.core.settings import settings
from cmt.models.suggestion import CommitSuggestion


class Cache:
    def __init__(self):
        self.cache_dir = Path(settings.CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _key(diff: str, model: str) -> str:
        return hashlib.sha256(f"{diff}-{model}".encode()).hexdigest()

    @staticmethod
    def _hashed_key(key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()

    def _set(self, diff: str, model: str, commit: CommitSuggestion):
        key = Cache._key(diff, model)
        cache_file = self.cache_dir / key
        cache_file.write_text(commit.model_dump_json())

    def _get(self, diff: str, model: str) -> CommitSuggestion | None:
        key = Cache._key(diff, model)
        cache_file = self.cache_dir / key
        if cache_file.exists():
            return CommitSuggestion(**json.loads(cache_file.read_text()))
        return None

    def set(self, key: str, value: str):
        cache_key = self._hashed_key(key)
        cache_file = self.cache_dir / cache_key
        cache_file.write_text(value)

    def get(self, key: str) -> str | None:
        cache_key = self._hashed_key(key)
        cache_file = self.cache_dir / cache_key
        if cache_file.exists():
            return cache_file.read_text()
        return None
