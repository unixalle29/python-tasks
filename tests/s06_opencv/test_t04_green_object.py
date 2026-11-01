import cv2
import numpy as np

from python_tasks.s06_opencv.t04_green_object import find_green_object


def test_finds_green_rectangle() -> None:
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    image[30:50, 20:60] = (0, 255, 0)
    assert find_green_object(image) == (20, 30, 40, 20)


def test_finds_green_circle() -> None:
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.circle(image, (50, 50), 10, (0, 255, 0), -1)
    x, y, width, height = find_green_object(image)
    assert 39 <= x <= 40
    assert 39 <= y <= 40
    assert 20 <= width <= 22
    assert 20 <= height <= 22


def test_returns_none_without_green() -> None:
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    assert find_green_object(image) is None


def test_ignores_red_object() -> None:
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    image[30:50, 20:60] = (0, 0, 255)
    assert find_green_object(image) is None
