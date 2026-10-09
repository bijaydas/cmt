import pytest

from cmt.models.changes import ChangeSet, File
from cmt.services.analyzer import Analyzer


def _analyze(*statuses: str):
    files = [File(status=s, path=f"f{i}.py") for i, s in enumerate(statuses)]
    return Analyzer().analyze(ChangeSet(files=files, diff=""))


def test_empty_change_set_returns_zeros():
    result = _analyze()

    assert result.model_dump() == {
        "total_files": 0,
        "added_files": 0,
        "modified_files": 0,
        "deleted_files": 0,
        "renamed_files": 0,
    }


@pytest.mark.parametrize(
    ("status", "field"),
    [
        ("A", "added_files"),
        ("M", "modified_files"),
        ("D", "deleted_files"),
        ("R", "renamed_files"),
    ],
)
def test_status_increments_matching_counter(status, field):
    result = _analyze(status)

    assert result.total_files == 1
    assert getattr(result, field) == 1


def test_unknown_status_counts_only_toward_total():
    result = _analyze("X")

    assert result.total_files == 1
    assert result.added_files == result.modified_files == 0
    assert result.deleted_files == result.renamed_files == 0


def test_analyzer_returns_analysis_result():
    change_sets = ChangeSet(
        files=[
            File(path="file1.txt", status="A"),
            File(path="file2.txt", status="M"),
            File(path="file3.txt", status="D"),
            File(path="file4.txt", status="R"),
        ],
        diff="test",
    )
    analyzer = Analyzer()
    result = analyzer.analyze(change_sets)

    assert result.total_files == 4
    assert result.added_files == 1
    assert result.modified_files == 1
    assert result.deleted_files == 1
    assert result.renamed_files == 1
