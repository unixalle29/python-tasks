import random

import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.animation import FuncAnimation

from python_tasks.s04_science.t05_random_walk import animate_walk, random_walk


def test_random_walk_shape_and_start() -> None:
    points, _ = random_walk(1000, random.Random(42))
    assert points.shape == (1001, 2)
    assert np.array_equal(points[0], [0, 0])


def test_random_walk_steps() -> None:
    points, _ = random_walk(1000, random.Random(42))
    differences = np.diff(points, axis=0)
    assert np.all(np.sum(np.abs(differences), axis=1) == 1)
    assert np.all(np.max(np.abs(differences), axis=1) == 1)


def test_random_walk_distance() -> None:
    points, distance = random_walk(1000, random.Random(42))
    assert distance == pytest.approx(np.linalg.norm(points[-1] - points[0]))


def test_random_walk_is_deterministic() -> None:
    first, _ = random_walk(100, random.Random(42))
    second, _ = random_walk(100, random.Random(42))
    assert np.array_equal(first, second)


def test_random_walk_changes_with_seed() -> None:
    first, _ = random_walk(100, random.Random(1))
    second, _ = random_walk(100, random.Random(2))
    assert not np.array_equal(first, second)


@pytest.mark.parametrize("steps", [0, -1])
def test_random_walk_rejects_non_positive_steps(steps: int) -> None:
    with pytest.raises(ValueError):
        random_walk(steps, random.Random(0))


def test_animate_walk_returns_animation() -> None:
    points, _ = random_walk(10, random.Random(42))
    animation = animate_walk(points)
    assert isinstance(animation, FuncAnimation)
    plt.close("all")
