from pathlib import Path

import pytest

from python_tasks.s03_files.t04_image_format import (
    JPEG_SIGNATURE,
    PNG_SIGNATURE,
    format_by_content,
    format_by_extension,
    inspect_file,
)


def write_file(tmp_path: Path, name: str, data: bytes) -> Path:
    path = tmp_path / name
    path.write_bytes(data)
    return path


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("image.png", "png"),
        ("image.PNG", "png"),
        ("image.jpg", "jpeg"),
        ("image.jpeg", "jpeg"),
        ("image.JPEG", "jpeg"),
        ("image.gif", "unknown"),
        ("image", "unknown"),
    ],
)
def test_format_by_extension(name: str, expected: str) -> None:
    assert format_by_extension(Path(name)) == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (PNG_SIGNATURE + b"payload", "png"),
        (JPEG_SIGNATURE + b"payload", "jpeg"),
        (b"plain text", "unknown"),
        (b"", "unknown"),
        (PNG_SIGNATURE[:-1], "unknown"),
    ],
)
def test_format_by_content(tmp_path: Path, data: bytes, expected: str) -> None:
    path = write_file(tmp_path, "file.bin", data)
    assert format_by_content(path) == expected


def test_inspect_matching_image(tmp_path: Path) -> None:
    path = write_file(tmp_path, "image.png", PNG_SIGNATURE + b"payload")
    assert inspect_file(path) == ("png", "png")


def test_inspect_mismatched_extension(tmp_path: Path) -> None:
    path = write_file(tmp_path, "image.jpg", PNG_SIGNATURE + b"payload")
    assert inspect_file(path) == ("jpeg", "png")


def test_inspect_unknown_file(tmp_path: Path) -> None:
    path = write_file(tmp_path, "file.txt", b"plain text")
    assert inspect_file(path) == ("unknown", "unknown")


def test_inspect_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        inspect_file(tmp_path / "missing.png")


def test_inspect_directory(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        inspect_file(tmp_path)
