from pathlib import Path

import pytest

from python_tasks.s05_gui.t03_editor import TextEditor


def test_open_and_save_file(qtbot, tmp_path: Path) -> None:
    editor = TextEditor()
    qtbot.addWidget(editor)
    source = tmp_path / "input.txt"
    source.write_text("привет", encoding="utf-8")
    editor.open_file(source)
    assert editor.editor.toPlainText() == "привет"
    editor.editor.setPlainText("новый текст")
    destination = tmp_path / "output.txt"
    editor.save_file(destination)
    assert destination.read_text(encoding="utf-8") == "новый текст"


def test_open_missing_file(qtbot, tmp_path: Path) -> None:
    editor = TextEditor()
    qtbot.addWidget(editor)
    with pytest.raises(FileNotFoundError):
        editor.open_file(tmp_path / "missing.txt")
