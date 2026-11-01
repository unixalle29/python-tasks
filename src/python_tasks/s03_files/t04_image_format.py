import sys
from pathlib import Path

REQUIRED_ARGUMENTS = 2

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SIGNATURE = b"\xff\xd8\xff"
JPEG_EXTENSIONS = (".jpg", ".jpeg")


def format_by_extension(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".png":
        return "png"
    if suffix in JPEG_EXTENSIONS:
        return "jpeg"
    return "unknown"


def format_by_content(path: Path) -> str:
    with path.open("rb") as file:
        header = file.read(10)
    if header.startswith(PNG_SIGNATURE):
        return "png"
    if header.startswith(JPEG_SIGNATURE):
        return "jpeg"
    return "unknown"


def inspect_file(path: Path) -> tuple[str, str]:
    if not path.is_file():
        raise FileNotFoundError(f"file not found: {path}")
    return format_by_extension(path), format_by_content(path)


def main() -> None:
    if len(sys.argv) != REQUIRED_ARGUMENTS:
        print("usage: python -m ... FILE", file=sys.stderr)
        raise SystemExit(2)
    try:
        extension, content = inspect_file(Path(sys.argv[1]))
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    print(f"extension: {extension}")
    print(f"content: {content}")
    if extension != content:
        print("warning: extension does not match content")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
