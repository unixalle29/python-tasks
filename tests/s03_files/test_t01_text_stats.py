from pathlib import Path

import pytest

from python_tasks.s03_files.t01_text_stats import (
    MAX_LENGTH,
    MIN_LENGTH,
    analyze_file,
    analyze_text,
    main,
)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello world\nSecond line", (20, 4, 2)),
        ("one\ntwo\nthree", (11, 3, 3)),
        ("  a\tb\n c ", (3, 3, 2)),
        ("", (0, 0, 0)),
        ("\n", (0, 0, 1)),
    ],
)
def test_analyze_text(text: str, expected: tuple[int, int, int]) -> None:
    assert analyze_text(text) == expected


@pytest.mark.parametrize(
    ("length", "is_valid"),
    [
        (MIN_LENGTH, True),
        (MAX_LENGTH, True),
        (MIN_LENGTH - 1, False),
        (MAX_LENGTH + 1, False),
        (0, False),
    ],
)
def test_analyze_file_checks_length(tmp_path: Path, length: int, is_valid: bool) -> None:
    path = tmp_path / "text.txt"
    path.write_text("a" * length, encoding="utf-8")
    if is_valid:
        assert analyze_file(path) == (length, 1 if length else 0, 1 if length else 0)
    else:
        with pytest.raises(ValueError):
            analyze_file(path)


def test_analyze_file_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        analyze_file(tmp_path / "missing.txt")


def test_analyze_file_rejects_invalid_utf8(tmp_path: Path) -> None:
    path = tmp_path / "binary.txt"
    path.write_bytes(b"\xff" * 100)
    with pytest.raises(UnicodeDecodeError):
        analyze_file(path)


def test_cli_output(tmp_path: Path, monkeypatch, capsys) -> None:
    path = tmp_path / "text.txt"
    path.write_text("a" * 100, encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["t01", str(path)])
    main()
    out = capsys.readouterr().out
    assert "characters: 100" in out
    assert "words: 1" in out
    assert "lines: 1" in out
