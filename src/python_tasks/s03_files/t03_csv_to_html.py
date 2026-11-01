import csv
import html
import sys
from pathlib import Path

REQUIRED_ARGUMENTS = 3

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>CSV table</title>
</head>
<body>
<table>
{rows}
</table>
</body>
</html>
"""


def read_csv(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8", newline="") as file:
        return [list(row) for row in csv.reader(file)]


def render_html(rows: list[list[str]]) -> str:
    lines = []
    for row in rows:
        cells = "".join(f"<td>{html.escape(cell)}</td>" for cell in row)
        lines.append(f"    <tr>{cells}</tr>")
    return HTML_TEMPLATE.format(rows="\n".join(lines))


def convert_csv(source: Path, destination: Path) -> None:
    destination.write_text(render_html(read_csv(source)), encoding="utf-8")


def main() -> None:
    if len(sys.argv) != REQUIRED_ARGUMENTS:
        print("usage: python -m ... INPUT.csv OUTPUT.html", file=sys.stderr)
        raise SystemExit(2)
    try:
        convert_csv(Path(sys.argv[1]), Path(sys.argv[2]))
    except (OSError, UnicodeError, csv.Error) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
