import sys
from pathlib import Path

import cv2
import numpy as np

LOWER_GREEN = np.array([40, 80, 80])
UPPER_GREEN = np.array([80, 255, 255])
REQUIRED_ARGUMENTS = 2


def find_green_object(image: np.ndarray) -> tuple[int, int, int, int] | None:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    contour = max(contours, key=cv2.contourArea)
    x, y, width, height = cv2.boundingRect(contour)
    return x, y, width, height


def main() -> None:
    if len(sys.argv) != REQUIRED_ARGUMENTS:
        print("usage: python -m ... IMAGE", file=sys.stderr)
        raise SystemExit(2)
    image = cv2.imread(str(Path(sys.argv[1])), cv2.IMREAD_COLOR)
    if image is None:
        print("error: cannot read image", file=sys.stderr)
        raise SystemExit(2)
    print(find_green_object(image))


if __name__ == "__main__":
    main()
