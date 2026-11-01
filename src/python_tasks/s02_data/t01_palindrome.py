import sys


def parse_text(raw: str) -> str:
    text = raw.strip()
    if not any(character.isalnum() for character in text):
        raise ValueError("text must contain at least one letter or digit")
    return text


def reverse_text(text: str) -> str:
    return text[::-1]


def is_palindrome(text: str) -> bool:
    normalized = "".join(character for character in text.casefold() if character.isalnum())
    return normalized == normalized[::-1]


def main() -> None:
    try:
        text = parse_text(sys.stdin.read())
        reversed_text = reverse_text(text)
        palindrome = is_palindrome(text)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    print(reversed_text)
    print("yes" if palindrome else "no")


if __name__ == "__main__":
    main()
