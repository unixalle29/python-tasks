import matplotlib.pyplot as plt
import numpy as np
import pytest

from python_tasks.s04_science.t02_surface import plot_surface, surface_values


@pytest.mark.parametrize(
    ("x", "y", "expected"),
    [
        pytest.param(0.0, 0.0, 0.0, id="origin"),
        pytest.param(np.pi / 2, 0.0, 1.0, id="peak"),
        pytest.param(0.0, np.pi, 0.0, id="zero-ring"),
        pytest.param(np.pi / 2, np.pi / 2, np.sin(np.sqrt(2) * np.pi / 2), id="combined"),
    ],
)
def test_surface_values(x: float, y: float, expected: float) -> None:
    result = surface_values(np.array([x]), np.array([y]))
    assert result[0] == pytest.approx(expected)


def test_surface_values_shape() -> None:
    coordinates = np.linspace(-5, 5, 20)
    x, y = np.meshgrid(coordinates, coordinates)
    assert surface_values(x, y).shape == (20, 20)


def test_plot_surface_returns_3d_figure() -> None:
    coordinates = np.linspace(-5, 5, 20)
    x, y = np.meshgrid(coordinates, coordinates)
    figure = plot_surface(x, y)
    assert len(figure.axes) == 1
    assert figure.axes[0].name == "3d"
    plt.close(figure)
