from html.parser import HTMLParser
from pathlib import Path

import pytest

from python_tasks.s03_files.t03_csv_to_html import convert_csv, read_csv, render_html


class TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self._row: list[str] | None = None
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tr":
            self._row = []
        elif tag == "td" and self._row is not None:
            self._cell = []

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "td" and self._row is not None and self._cell is not None:
            self._row.append("".join(self._cell))
            self._cell = None
        elif tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None


def test_read_csv_with_quoted_values(tmp_path: Path) -> None:
    path = tmp_path / "table.csv"
    path.write_text('name,score\n"Smith, John",10\n"say ""hi""",20\n', encoding="utf-8")
    assert read_csv(path) == [["name", "score"], ["Smith, John", "10"], ['say "hi"', "20"]]


def test_read_csv_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_csv(tmp_path / "missing.csv")


def test_render_html_escapes_values() -> None:
    result = render_html([["<b>", "a&b", 'quote"']])
    assert "&lt;b&gt;" in result
    assert "a&amp;b" in result
    assert "&quot;" in result


def test_convert_csv_roundtrip(tmp_path: Path) -> None:
    source = tmp_path / "table.csv"
    destination = tmp_path / "table.html"
    source.write_text('a,"b,c"\n"line1\nline2",d\n', encoding="utf-8")
    convert_csv(source, destination)
    parser = TableParser()
    parser.feed(destination.read_text(encoding="utf-8"))
    assert parser.rows == [["a", "b,c"], ["line1\nline2", "d"]]


def test_convert_empty_csv(tmp_path: Path) -> None:
    source = tmp_path / "empty.csv"
    destination = tmp_path / "empty.html"
    source.write_text("", encoding="utf-8")
    convert_csv(source, destination)
    parser = TableParser()
    parser.feed(destination.read_text(encoding="utf-8"))
    assert parser.rows == []
