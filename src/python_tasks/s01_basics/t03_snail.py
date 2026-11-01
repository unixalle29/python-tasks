import sys

ARGUMENT_COUNT = 3
MIN_VALUE = 1


def _require_positive(name: str, value: int) -> None:
    if value < MIN_VALUE:
        raise ValueError(f"{name} must be positive")


def parse_arguments(raw: str) -> tuple[int, int, int]:
    tokens = raw.split()
    if len(tokens) != ARGUMENT_COUNT:
        raise ValueError(f"expected {ARGUMENT_COUNT} integers, got {len(tokens)}")
    try:
        values = tuple(int(token) for token in tokens)
    except ValueError as exc:
        raise ValueError("arguments must be integers") from exc
    height, climb, slide = values
    _require_positive("height", height)
    _require_positive("climb", climb)
    _require_positive("slide", slide)
    return height, climb, slide


def days_to_top(height: int, climb: int, slide: int) -> int:
    if climb >= height:
        return 1
    if climb <= slide:
        raise ValueError("the snail will never reach the top")
    progress = climb - slide
    remaining = height - climb
    return 1 + (remaining + progress - 1) // progress


def main() -> None:
    try:
        height, climb, slide = parse_arguments(sys.stdin.read())
        days = days_to_top(height, climb, slide)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    print(days)


if __name__ == "__main__":
    main()
