import base64
import sys
from pathlib import Path

ENCRYPT_ARGUMENTS = 4
DECRYPT_ARGUMENTS = 3


def key_bytes(key: str) -> bytes:
    if not key:
        raise ValueError("key must not be empty")
    return key.encode("utf-8")


def encrypt_text(text: str, key: str) -> str:
    key_data = key_bytes(key)
    data = text.encode("utf-8")
    encrypted = bytes(byte ^ key_data[index % len(key_data)] for index, byte in enumerate(data))
    return base64.b64encode(encrypted).decode("ascii")


def decrypt_text(token: str, key: str) -> str:
    key_data = key_bytes(key)
    try:
        encrypted = base64.b64decode(token, validate=True)
    except ValueError as exc:
        raise ValueError("invalid encoded text") from exc
    data = bytes(byte ^ key_data[index % len(key_data)] for index, byte in enumerate(encrypted))
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("wrong key or corrupted text") from exc


def encrypt_file(source: Path, destination: Path, key: str) -> None:
    destination.write_text(encrypt_text(source.read_text(encoding="utf-8"), key), encoding="utf-8")


def decrypt_file(source: Path, destination: Path, key: str) -> None:
    destination.write_text(decrypt_text(source.read_text(encoding="utf-8"), key), encoding="utf-8")


def main() -> None:
    if len(sys.argv) < DECRYPT_ARGUMENTS:
        print("usage: python -m ... encrypt|decrypt ...", file=sys.stderr)
        raise SystemExit(2)
    command = sys.argv[1]
    if command not in ("encrypt", "decrypt"):
        print("error: command must be 'encrypt' or 'decrypt'", file=sys.stderr)
        raise SystemExit(2)
    if command == "encrypt" and len(sys.argv) != ENCRYPT_ARGUMENTS:
        print("usage: python -m ... encrypt INPUT OUTPUT", file=sys.stderr)
        raise SystemExit(2)
    if command == "decrypt" and len(sys.argv) != DECRYPT_ARGUMENTS:
        print("usage: python -m ... decrypt INPUT", file=sys.stderr)
        raise SystemExit(2)
    key = input("Ключ: ")
    try:
        if command == "encrypt":
            encrypt_file(Path(sys.argv[2]), Path(sys.argv[3]), key)
        else:
            token = Path(sys.argv[2]).read_text(encoding="utf-8")
            print(decrypt_text(token, key))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
