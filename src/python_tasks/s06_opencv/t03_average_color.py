import sys
from pathlib import Path

import cv2
import numpy as np

SQUARE_SIZE = 200
REQUIRED_ARGUMENTS = 2


def average_color(image: np.ndarray) -> tuple[int, int, int]:
    height, width = image.shape[:2]
    mean = image.reshape(height * width, 3).mean(axis=0)
    blue, green, red = mean
    return round(blue), round(green), round(red)


def color_square(color: tuple[int, int, int], size: int = SQUARE_SIZE) -> np.ndarray:
    if size < 1:
        raise ValueError("size must be positive")
    return np.full((size, size, 3), color, dtype=np.uint8)


def main() -> None:
    if len(sys.argv) != REQUIRED_ARGUMENTS:
        print("usage: python -m ... IMAGE", file=sys.stderr)
        raise SystemExit(2)
    image = cv2.imread(str(Path(sys.argv[1])), cv2.IMREAD_COLOR)
    if image is None:
        print("error: cannot read image", file=sys.stderr)
        raise SystemExit(2)
    square = color_square(average_color(image))
    cv2.imshow("Average color", square)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
