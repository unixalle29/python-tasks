import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

T_MIN = -4.0
T_MAX = 4.0
POINT_COUNT = 400


def complex_values(t: np.ndarray) -> np.ndarray:
    return 1 / (1 + 1j * t)


def plot_complex_values(t: np.ndarray) -> Figure:
    values = complex_values(t)
    figure, axes = plt.subplots()
    scatter = axes.scatter(
        values.real,
        values.imag,
        c=np.abs(values),
        cmap="viridis",
    )
    figure.colorbar(scatter, ax=axes)
    axes.set_xlabel("Re(f)")
    axes.set_ylabel("Im(f)")
    return figure


def main() -> None:
    t = np.linspace(T_MIN, T_MAX, POINT_COUNT)
    plot_complex_values(t)
    plt.show()


if __name__ == "__main__":
    main()
