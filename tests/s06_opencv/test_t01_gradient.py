import numpy as np
import pytest

from python_tasks.s06_opencv.t01_gradient import BLACK, GRAY, SIZE, WHITE, gradient_image


def test_default_size_and_type() -> None:
    image = gradient_image()
    assert image.shape == (SIZE, SIZE)
    assert image.dtype == np.uint8


def test_corner_values() -> None:
    image = gradient_image()
    assert image[0, 0] == GRAY
    assert image[-1, -1] == GRAY
    assert image[0, -1] == WHITE
    assert image[-1, 0] == BLACK


def test_gradient_is_diagonal() -> None:
    image = gradient_image()
    assert np.all(image[0] >= GRAY)
    assert np.all(image[:, 0] <= GRAY)
    assert np.all(np.diff(image[0].astype(int)) >= 0)
    assert np.all(np.diff(image[:, 0].astype(int)) <= 0)


@pytest.mark.parametrize("size", [0, 1, -1])
def test_rejects_too_small_size(size: int) -> None:
    with pytest.raises(ValueError):
        gradient_image(size)
