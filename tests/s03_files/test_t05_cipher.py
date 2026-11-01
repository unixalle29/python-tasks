from pathlib import Path

import pytest

from python_tasks.s03_files.t05_cipher import decrypt_file, decrypt_text, encrypt_file, encrypt_text


@pytest.mark.parametrize(
    "text",
    ["", "Hello, world!", "Привет, мир!", "emoji 🐍"],
)
def test_roundtrip(text: str) -> None:
    assert decrypt_text(encrypt_text(text, "secret"), "secret") == text


def test_wrong_key_gives_different_text() -> None:
    token = encrypt_text("hello", "secret")
    assert decrypt_text(token, "another") != "hello"


def test_decrypt_rejects_invalid_base64() -> None:
    with pytest.raises(ValueError):
        decrypt_text("not base64!", "secret")


def test_empty_key_is_rejected() -> None:
    with pytest.raises(ValueError):
        encrypt_text("text", "")
    with pytest.raises(ValueError):
        decrypt_text("token", "")


def test_file_roundtrip(tmp_path: Path) -> None:
    source = tmp_path / "plain.txt"
    encrypted = tmp_path / "encrypted.txt"
    decrypted = tmp_path / "decrypted.txt"
    source.write_text("секретный текст", encoding="utf-8")
    encrypt_file(source, encrypted, "ключ")
    decrypt_file(encrypted, decrypted, "ключ")
    assert decrypted.read_text(encoding="utf-8") == "секретный текст"


def test_encrypt_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        encrypt_file(tmp_path / "missing.txt", tmp_path / "out.txt", "key")
