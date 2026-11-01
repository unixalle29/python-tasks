import math
import sys

COORDINATE_COUNT = 4


def parse_coordinates(raw: str) -> tuple[float, float, float, float]:
    tokens = raw.split()
    if len(tokens) != COORDINATE_COUNT:
        raise ValueError(f"expected {COORDINATE_COUNT} coordinates, got {len(tokens)}")
    try:
        coordinates = tuple(float(token) for token in tokens)
    except ValueError as exc:
        raise ValueError("coordinates must be numbers") from exc
    if not all(math.isfinite(value) for value in coordinates):
        raise ValueError("coordinates must be finite")
    x1, y1, x2, y2 = coordinates
    return x1, y1, x2, y2


def line_coefficients(x1: float, y1: float, x2: float, y2: float) -> tuple[float, float]:
    if x1 == x2:
        raise ValueError("the line is vertical or the points coincide")
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    if not math.isfinite(slope) or not math.isfinite(intercept):
        raise ValueError("the line coefficients are not finite")
    return slope, intercept


def main() -> None:
    try:
        x1, y1, x2, y2 = parse_coordinates(sys.stdin.read())
        slope, intercept = line_coefficients(x1, y1, x2, y2)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    print(slope, intercept)


if __name__ == "__main__":
    main()
