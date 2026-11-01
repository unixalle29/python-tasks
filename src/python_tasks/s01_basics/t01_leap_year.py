import sys

MIN_YEAR = 1
LEAP_STEP = 4
CENTURY = 100
LEAP_CENTURY = 400


def parse_year(raw: str) -> int:
    try:
        year = int(raw.strip())
    except ValueError as exc:
        raise ValueError("year must be an integer") from exc
    if year < MIN_YEAR:
        raise ValueError(f"year must be at least {MIN_YEAR}")
    return year


def is_leap_year(year: int) -> bool:
    return year % LEAP_STEP == 0 and (year % CENTURY != 0 or year % LEAP_CENTURY == 0)


def main() -> None:
    try:
        year = parse_year(sys.stdin.read())
        result = is_leap_year(year)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    print("yes" if result else "no")


if __name__ == "__main__":
    main()
