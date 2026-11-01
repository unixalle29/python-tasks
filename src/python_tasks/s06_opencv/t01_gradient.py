import numpy as np

MIN_SIZE = 2
SIZE = 100
WHITE = 255
GRAY = 128
BLACK = 0


def gradient_image(size: int = SIZE) -> np.ndarray:
    if size < MIN_SIZE:
        raise ValueError("size must be at least 2")
    rows, cols = np.meshgrid(np.arange(size), np.arange(size), indexing="ij")
    upper = GRAY + (WHITE - GRAY) * (cols - rows) / (size - 1)
    lower = GRAY + (GRAY - BLACK) * (cols - rows) / (size - 1)
    values = np.where(cols >= rows, upper, lower)
    return np.clip(np.rint(values), 0, 255).astype(np.uint8)
