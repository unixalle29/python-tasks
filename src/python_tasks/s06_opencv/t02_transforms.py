import sys
from pathlib import Path
from typing import cast

import cv2
import numpy as np

SCALE = 1.5
ANGLE = 10.0
REQUIRED_ARGUMENTS = 3


def load_image(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"cannot read image: {path}")
    return cast("np.ndarray", image)


def save_image(path: Path, image: np.ndarray) -> None:
    if not cv2.imwrite(str(path), image):
        raise ValueError(f"cannot write image: {path}")


def resize_image(image: np.ndarray) -> np.ndarray:
    result = cv2.resize(image, None, fx=SCALE, fy=SCALE, interpolation=cv2.INTER_LINEAR)
    return cast("np.ndarray", result)


def mirror_image(image: np.ndarray) -> np.ndarray:
    return cast("np.ndarray", cv2.flip(image, 1))


def rotate_image(image: np.ndarray, angle: float = ANGLE) -> np.ndarray:
    height, width = image.shape[:2]
    center = (width / 2, height / 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cast("np.ndarray", cv2.warpAffine(image, matrix, (width, height)))


def transform_image(image: np.ndarray) -> np.ndarray:
    return rotate_image(mirror_image(resize_image(image)))


def main() -> None:
    if len(sys.argv) != REQUIRED_ARGUMENTS:
        print("usage: python -m ... INPUT OUTPUT", file=sys.stderr)
        raise SystemExit(2)
    try:
        save_image(Path(sys.argv[2]), transform_image(load_image(Path(sys.argv[1]))))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
