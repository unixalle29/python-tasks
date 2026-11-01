from pathlib import Path

import pytest

from python_tasks.s03_files.t06_grep import search_directory, search_text, total_occurrences


@pytest.mark.parametrize(
    ("text", "needle", "expected"),
    [
        ("foo bar\nbaz foo foo", "foo", [(1, "foo bar", 1), (2, "baz foo foo", 2)]),
        ("foo\nbar", "missing", []),
        ("FOO\nfoo", "foo", [(2, "foo", 1)]),
        ("aaaa", "aa", [(1, "aaaa", 2)]),
        ("", "foo", []),
    ],
)
def test_search_text(text: str, needle: str, expected: list[tuple[int, str, int]]) -> None:
    assert search_text(text, needle) == expected


def test_search_text_rejects_empty_needle() -> None:
    with pytest.raises(ValueError):
        search_text("text", "")


def test_search_directory(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("foo\nbar foo\n", encoding="utf-8")
    (tmp_path / "b.txt").write_text("FOO\n", encoding="utf-8")
    (tmp_path / "binary.bin").write_bytes(b"\xfffoo")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "c.txt").write_text("foo\n", encoding="utf-8")
    results = search_directory(tmp_path, "foo")
    assert [(path.name, line_number, line, count) for path, line_number, line, count in results] == [
        ("a.txt", 1, "foo", 1),
        ("a.txt", 2, "bar foo", 1),
    ]
    assert total_occurrences(results) == 2


def test_search_directory_rejects_missing_directory(tmp_path: Path) -> None:
    with pytest.raises(NotADirectoryError):
        search_directory(tmp_path / "missing", "foo")
