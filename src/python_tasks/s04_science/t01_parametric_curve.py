import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

T_START = 0.0
T_END = 4.0 * np.pi
POINT_COUNT = 400


def curve_parameters(t: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = t**2 * np.sin(t)
    y = t**2 * np.cos(t)
    z = t**2
    return x, y, z


def plot_curve(t: np.ndarray) -> Figure:
    x, y, z = curve_parameters(t)
    figure = plt.figure()
    axes = figure.add_subplot(projection="3d")
    axes.plot(x, y, z)
    axes.set_xlabel("x")
    axes.set_ylabel("y")
    axes.set_zlabel("z")
    return figure


def main() -> None:
    t = np.linspace(T_START, T_END, POINT_COUNT)
    plot_curve(t)
    plt.show()


if __name__ == "__main__":
    main()
