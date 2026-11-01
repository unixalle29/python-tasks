import numpy as np
import pytest

from python_tasks.s06_opencv.t03_average_color import average_color, color_square


def test_average_color_of_solid_image() -> None:
    image = np.full((10, 10, 3), (255, 0, 0), dtype=np.uint8)
    assert average_color(image) == (255, 0, 0)


def test_average_color_of_two_colors() -> None:
    image = np.zeros((2, 2, 3), dtype=np.uint8)
    image[:1] = (0, 0, 255)
    image[1:] = (0, 255, 0)
    assert average_color(image) == (0, 128, 128)


def test_color_square() -> None:
    square = color_square((0, 255, 0), size=50)
    assert square.shape == (50, 50, 3)
    assert np.all(square == (0, 255, 0))


@pytest.mark.parametrize("size", [0, -1])
def test_color_square_rejects_non_positive_size(size: int) -> None:
    with pytest.raises(ValueError):
        color_square((0, 255, 0), size)
