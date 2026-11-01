from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

SURFACE_MIN = -5.0
SURFACE_MAX = 5.0
GRID_SIZE = 200


def surface_values(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return cast("np.ndarray", np.sin(np.sqrt(x**2 + y**2)))


def plot_surface(x: np.ndarray, y: np.ndarray) -> Figure:
    figure = plt.figure()
    axes = figure.add_subplot(projection="3d")
    axes.plot_surface(x, y, surface_values(x, y), cmap="viridis")
    axes.set_xlabel("x")
    axes.set_ylabel("y")
    axes.set_zlabel("z")
    return figure


def main() -> None:
    coordinates = np.linspace(SURFACE_MIN, SURFACE_MAX, GRID_SIZE)
    x, y = np.meshgrid(coordinates, coordinates)
    plot_surface(x, y)
    plt.show()


if __name__ == "__main__":
    main()
