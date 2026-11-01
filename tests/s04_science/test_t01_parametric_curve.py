import matplotlib.pyplot as plt
import numpy as np
import pytest

from python_tasks.s04_science.t01_parametric_curve import curve_parameters, plot_curve


@pytest.mark.parametrize(
    ("t", "expected"),
    [
        pytest.param(0.0, (0.0, 0.0, 0.0), id="origin"),
        pytest.param(1.0, (np.sin(1.0), np.cos(1.0), 1.0), id="unit"),
        pytest.param(
            np.pi / 2,
            ((np.pi / 2) ** 2, 0.0, (np.pi / 2) ** 2),
            id="quarter-turn",
        ),
    ],
)
def test_curve_parameters(t: float, expected: tuple[float, float, float]) -> None:
    x, y, z = curve_parameters(np.array([t]))
    assert x[0] == pytest.approx(expected[0])
    assert y[0] == pytest.approx(expected[1])
    assert z[0] == pytest.approx(expected[2])


def test_plot_curve_returns_3d_figure() -> None:
    figure = plot_curve(np.linspace(0, 1, 10))
    assert len(figure.axes) == 1
    assert figure.axes[0].name == "3d"
    plt.close(figure)
