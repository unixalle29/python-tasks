TARGET_TERM = 1000
FIRST_TERM = 1


def nth_fibonacci(n: int) -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < FIRST_TERM:
        raise ValueError(f"n must be at least {FIRST_TERM}")
    previous, current = 0, 1
    for _ in range(n - FIRST_TERM):
        previous, current = current, previous + current
    return previous


def main() -> None:
    print(nth_fibonacci(TARGET_TERM))


if __name__ == "__main__":
    main()
