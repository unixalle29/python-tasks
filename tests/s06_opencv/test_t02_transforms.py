from pathlib import Path

import numpy as np
import pytest

from python_tasks.s06_opencv.t02_transforms import (
    load_image,
    mirror_image,
    resize_image,
    rotate_image,
    save_image,
    transform_image,
)


def make_image() -> np.ndarray:
    image = np.zeros((4, 6, 3), dtype=np.uint8)
    image[:, :3] = (0, 0, 255)
    image[:, 3:] = (255, 0, 0)
    return image


def test_resize_image() -> None:
    resized = resize_image(make_image())
    assert resized.shape == (6, 9, 3)


def test_mirror_image() -> None:
    mirrored = mirror_image(make_image())
    assert np.all(mirrored[:, 0] == (255, 0, 0))
    assert np.all(mirrored[:, -1] == (0, 0, 255))


def test_rotate_image_keeps_shape() -> None:
    rotated = rotate_image(make_image())
    assert rotated.shape == (4, 6, 3)


def test_transform_image_shape() -> None:
    transformed = transform_image(make_image())
    assert transformed.shape == (6, 9, 3)


def test_save_and_load_image(tmp_path: Path) -> None:
    path = tmp_path / "image.png"
    save_image(path, make_image())
    loaded = load_image(path)
    assert loaded.shape == (4, 6, 3)


def test_load_missing_image(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        load_image(tmp_path / "missing.png")


def test_save_to_missing_directory(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        save_image(tmp_path / "missing" / "image.png", make_image())
