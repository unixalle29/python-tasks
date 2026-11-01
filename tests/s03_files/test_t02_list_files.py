from pathlib import Path

import pytest

from python_tasks.s03_files.t02_list_files import format_file, list_files, main


def test_list_files_sorts_and_skips_directories(tmp_path: Path) -> None:
    (tmp_path / "b.py").write_text("", encoding="utf-8")
    (tmp_path / "A.txt").write_text("", encoding="utf-8")
    (tmp_path / "c.PY").write_text("", encoding="utf-8")
    (tmp_path / "directory").mkdir()
    files = list_files(tmp_path)
    assert [path.name for path in files] == ["A.txt", "b.py", "c.PY"]
    assert [format_file(path) for path in files] == ["   A.txt", "-> b.py", "-> c.PY"]


def test_list_files_rejects_missing_directory(tmp_path: Path) -> None:
    with pytest.raises(NotADirectoryError):
        list_files(tmp_path / "missing")


def test_list_files_rejects_file_path(tmp_path: Path) -> None:
    path = tmp_path / "file.txt"
    path.write_text("", encoding="utf-8")
    with pytest.raises(NotADirectoryError):
        list_files(path)


def test_cli_output(tmp_path: Path, monkeypatch, capsys) -> None:
    (tmp_path / "script.py").write_text("", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["t02", str(tmp_path)])
    main()
    out = capsys.readouterr().out.splitlines()
    assert "-> script.py" in out
    assert "   notes.txt" in out
