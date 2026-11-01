import sys
from pathlib import Path


def list_files(directory: Path) -> list[Path]:
    if not directory.is_dir():
        raise NotADirectoryError(f"not a directory: {directory}")
    files = [path for path in directory.iterdir() if path.is_file()]
    return sorted(files, key=lambda path: path.name.lower())


def format_file(path: Path) -> str:
    marker = "-> " if path.suffix.lower() == ".py" else "   "
    return marker + path.name


def main() -> None:
    directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    try:
        files = list_files(directory)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    for path in files:
        print(format_file(path))


if __name__ == "__main__":
    main()
