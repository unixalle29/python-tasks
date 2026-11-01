import matplotlib.pyplot as plt
import numpy as np
import pytest

from python_tasks.s04_science.t03_complex_plot import complex_values, plot_complex_values


@pytest.mark.parametrize(
    ("t", "expected"),
    [
        pytest.param(0.0, 1 + 0j, id="real-axis"),
        pytest.param(1.0, 0.5 - 0.5j, id="unit"),
        pytest.param(-1.0, 0.5 + 0.5j, id="conjugate"),
        pytest.param(4.0, 1 / 17 - 4j / 17, id="boundary"),
    ],
)
def test_complex_values(t: float, expected: complex) -> None:
    result = complex_values(np.array([t]))
    assert result[0] == pytest.approx(expected)


def test_complex_magnitude_decreases_with_t() -> None:
    values = complex_values(np.array([0.0, 1.0, 4.0]))
    assert np.all(np.diff(np.abs(values)) < 0)


def test_plot_complex_values_returns_figure_with_colorbar() -> None:
    figure = plot_complex_values(np.linspace(-4, 4, 100))
    assert len(figure.axes) == 2
    plt.close(figure)
