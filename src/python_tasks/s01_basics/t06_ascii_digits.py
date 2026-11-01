import sys

GLYPH_HEIGHT = 5
DIGIT_GLYPHS: dict[str, tuple[str, ...]] = {
    "0": ("***", "* *", "* *", "* *", "***"),
    "1": (" * ", "** ", " * ", " * ", "***"),
    "2": ("***", "  *", "***", "*  ", "***"),
    "3": ("***", "  *", "***", "  *", "***"),
    "4": ("* *", "* *", "***", "  *", "  *"),
    "5": ("***", "*  ", "***", "  *", "***"),
    "6": ("***", "*  ", "***", "* *", "***"),
    "7": ("***", "  *", " * ", " * ", " * "),
    "8": ("***", "* *", "***", "* *", "***"),
    "9": ("***", "* *", "***", "  *", "***"),
    "-": ("   ", "   ", "***", "   ", "   "),
}


def parse_number(raw: str) -> int:
    try:
        number = int(raw.strip())
    except ValueError as exc:
        raise ValueError("number must be an integer") from exc
    return number


def render_number(number: int) -> str:
    glyphs = [DIGIT_GLYPHS[character] for character in str(number)]
    return "\n".join(" ".join(glyph[row] for glyph in glyphs) for row in range(GLYPH_HEIGHT))


def main() -> None:
    try:
        number = parse_number(sys.stdin.read())
        rendered = render_number(number)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    print(rendered)


if __name__ == "__main__":
    main()
