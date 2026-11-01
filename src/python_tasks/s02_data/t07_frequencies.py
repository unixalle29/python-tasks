import random
from collections import Counter
from collections.abc import Iterable

SEQUENCE_LENGTH = 1_000_000
MIN_VALUE = 1
MAX_VALUE = 50


def count_frequencies(values: Iterable[int], maximum: int) -> list[tuple[int, int]]:
    if maximum < 1:
        raise ValueError("maximum must be positive")
    frequencies = Counter(values)
    if any(number < MIN_VALUE or number > maximum for number in frequencies):
        raise ValueError("values must be within the requested range")
    for number in range(MIN_VALUE, maximum + 1):
        frequencies.setdefault(number, 0)
    return sorted(frequencies.items(), key=lambda item: (-item[1], item[0]))


def generate_frequencies(
    count: int,
    rng: random.Random,
    maximum: int = MAX_VALUE,
) -> list[tuple[int, int]]:
    if count < 0:
        raise ValueError("count must be non-negative")
    if maximum < 1:
        raise ValueError("maximum must be positive")
    values = (rng.randint(MIN_VALUE, maximum) for _ in range(count))
    return count_frequencies(values, maximum)


def main() -> None:
    for number, count in generate_frequencies(SEQUENCE_LENGTH, random.Random()):
        print(f"{number}: {count}")


if __name__ == "__main__":
    main()
