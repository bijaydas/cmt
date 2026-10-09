from cmt.models.changes import AnalysisResult, ChangeSet, File
from cmt.services.prompt import PromptService

ANALYSIS = AnalysisResult(
    total_files=2, added_files=1, modified_files=1, deleted_files=0, renamed_files=0
)
CHANGE_SET = ChangeSet(
    files=[File(status="A", path="new.py"), File(status="M", path="old.py")],
    diff="UNIQUE_DIFF_MARKER",
)


def _text(prompt) -> str:
    return "\n".join(m.content for m in prompt.to_messages())


def test_stringify_files_empty():
    assert PromptService()._stringify_files([]) == ""


def test_stringify_files_one_line_per_file_without_trailing_newline():
    files = [File(status="A", path="a.py"), File(status="D", path="b.py")]

    assert PromptService()._stringify_files(files) == "A a.py\nD b.py"


def test_commit_prompt_contains_diff_and_files():
    text = _text(PromptService().get_commit_prompt(CHANGE_SET, ANALYSIS))

    assert "UNIQUE_DIFF_MARKER" in text
    assert "A new.py" in text
    assert "M old.py" in text


def test_summary_prompt_contains_diff_and_files():
    text = _text(PromptService().get_summary_prompt(CHANGE_SET, ANALYSIS))

    assert "UNIQUE_DIFF_MARKER" in text
    assert "A new.py" in text
    assert "M old.py" in text
