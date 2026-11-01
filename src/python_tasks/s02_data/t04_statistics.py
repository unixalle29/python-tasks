import math
import random
import sys
from collections.abc import Sequence

LOWER_BOUND = 0.0
UPPER_BOUND = 10.0


def parse_count(raw: str) -> int:
    try:
        count = int(raw.strip())
    except ValueError as exc:
        raise ValueError("count must be an integer") from exc
    if count < 1:
        raise ValueError("count must be positive")
    return count


def generate_values(count: int, rng: random.Random) -> list[float]:
    if count < 1:
        raise ValueError("count must be positive")
    return [rng.uniform(LOWER_BOUND, UPPER_BOUND) for _ in range(count)]


def mean(values: Sequence[float]) -> float:
    if not values:
        raise ValueError("values must not be empty")
    return sum(values) / len(values)


def root_sum_squared_deviations(values: Sequence[float]) -> float:
    average = mean(values)
    return math.sqrt(sum((value - average) ** 2 for value in values))


def main() -> None:
    try:
        count = parse_count(sys.stdin.read())
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    values = generate_values(count, random.Random())
    print(f"{mean(values):.6f} {root_sum_squared_deviations(values):.6f}")


if __name__ == "__main__":
    main()
