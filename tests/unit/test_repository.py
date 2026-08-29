from cmt.git.repository import Repository


def test_invalid_git_repository(tmp_path):
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()

    repo = Repository(tmp_path)

    assert repo.is_git_repository() is False


def test_valid_git_repository(tmp_path):
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()

    # Initialize a git repository
    import subprocess

    subprocess.run(["git", "init"], cwd=repo_path)

    repo = Repository(repo_path)

    assert repo.is_git_repository() is True
