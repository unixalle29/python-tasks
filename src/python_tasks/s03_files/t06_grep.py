import sys
from pathlib import Path

MIN_ARGUMENTS = 2
MAX_ARGUMENTS = 3


def search_text(text: str, needle: str) -> list[tuple[int, str, int]]:
    if not needle:
        raise ValueError("search string must not be empty")
    matches = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        occurrences = line.count(needle)
        if occurrences:
            matches.append((line_number, line, occurrences))
    return matches


def search_directory(directory: Path, needle: str) -> list[tuple[Path, int, str, int]]:
    if not directory.is_dir():
        raise NotADirectoryError(f"not a directory: {directory}")
    results = []
    for path in sorted(directory.iterdir()):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        for line_number, line, occurrences in search_text(text, needle):
            results.append((path, line_number, line, occurrences))
    return results


def total_occurrences(results: list[tuple[Path, int, str, int]]) -> int:
    return sum(result[3] for result in results)


def main() -> None:
    if not MIN_ARGUMENTS <= len(sys.argv) <= MAX_ARGUMENTS:
        print("usage: python -m ... NEEDLE [DIRECTORY]", file=sys.stderr)
        raise SystemExit(2)
    needle = sys.argv[1]
    directory = Path(sys.argv[2]) if len(sys.argv) == MAX_ARGUMENTS else Path.cwd()
    try:
        results = search_directory(directory, needle)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    for path, line_number, line, _ in results:
        print(f"{path.name}:{line_number}: {line}")
    print(f"occurrences: {total_occurrences(results)}")


if __name__ == "__main__":
    main()
