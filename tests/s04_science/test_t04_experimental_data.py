from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pytest

from python_tasks.s04_science.t04_experimental_data import plot_measurements, read_measurements


def test_read_measurements(tmp_path: Path) -> None:
    path = tmp_path / "data.txt"
    path.write_text("1 2 4\n2 3 5 7\n", encoding="utf-8")
    x, means, errors = read_measurements(path)
    assert np.array_equal(x, [1.0, 2.0])
    assert means == pytest.approx([3.0, 5.0])
    assert errors == pytest.approx([1.0, np.std([3.0, 5.0, 7.0])])


def test_read_measurements_skips_blank_lines(tmp_path: Path) -> None:
    path = tmp_path / "data.txt"
    path.write_text("\n1 5\n\n2 6\n", encoding="utf-8")
    x, means, _ = read_measurements(path)
    assert np.array_equal(x, [1.0, 2.0])
    assert means == pytest.approx([5.0, 6.0])


def test_single_measurement_has_zero_error(tmp_path: Path) -> None:
    path = tmp_path / "data.txt"
    path.write_text("1 5\n2 6\n", encoding="utf-8")
    _, _, errors = read_measurements(path)
    assert errors == pytest.approx([0.0, 0.0])


@pytest.mark.parametrize(
    "content",
    ["", "1\n", "1 a\n", "1 nan\n", "1 inf\n"],
)
def test_read_measurements_rejects_invalid_files(tmp_path: Path, content: str) -> None:
    path = tmp_path / "data.txt"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ValueError):
        read_measurements(path)


def test_read_measurements_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_measurements(tmp_path / "missing.txt")


def test_plot_measurements_returns_figure() -> None:
    plot_measurements(np.array([1.0, 2.0]), np.array([3.0, 4.0]), np.array([0.1, 0.2]))
    figure = plt.gcf()
    assert len(figure.axes) == 1
    plt.close(figure)
