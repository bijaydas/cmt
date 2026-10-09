from cmt.models.changes import ChangeSet, File
from cmt.services.analyzer import Analyzer


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
