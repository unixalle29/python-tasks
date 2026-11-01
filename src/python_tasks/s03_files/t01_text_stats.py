import sys
from pathlib import Path

REQUIRED_ARGUMENTS = 2
MIN_LENGTH = 100
MAX_LENGTH = 1000


def analyze_text(text: str) -> tuple[int, int, int]:
    characters = sum(1 for character in text if not character.isspace())
    words = len(text.split())
    lines = len(text.splitlines())
    return characters, words, lines


def analyze_file(path: Path) -> tuple[int, int, int]:
    text = path.read_text(encoding="utf-8")
    if not MIN_LENGTH <= len(text) <= MAX_LENGTH:
        raise ValueError(f"text must contain {MIN_LENGTH}-{MAX_LENGTH} characters")
    return analyze_text(text)


def main() -> None:
    if len(sys.argv) != REQUIRED_ARGUMENTS:
        print("usage: python -m ... FILE", file=sys.stderr)
        raise SystemExit(2)
    try:
        characters, words, lines = analyze_file(Path(sys.argv[1]))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    print(f"characters: {characters}")
    print(f"words: {words}")
    print(f"lines: {lines}")


if __name__ == "__main__":
    main()
