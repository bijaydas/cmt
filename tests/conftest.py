import subprocess

import pytest

from cmt.core.settings import settings


@pytest.fixture
def git_repo(tmp_path):
    def run(*args):
        subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True)

    run("init")
    run("config", "user.email", "me@bijaydas.com")
    run("config", "user.name", "Bijay Das")
    return tmp_path


@pytest.fixture
def cache_dir(tmp_path, monkeypatch):
    path = tmp_path / "cache"
    monkeypatch.setattr(settings, "CACHE_DIR", str(path))
    return path
