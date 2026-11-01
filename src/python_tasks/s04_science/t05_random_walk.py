import random

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

STEPS = 1000
INTERVAL = 10


def random_walk(steps: int, rng: random.Random) -> tuple[np.ndarray, float]:
    if steps < 1:
        raise ValueError("steps must be positive")
    points = np.zeros((steps + 1, 2), dtype=int)
    for index in range(1, steps + 1):
        points[index] = points[index - 1]
        axis = rng.randrange(2)
        points[index, axis] += rng.choice((-1, 1))
    distance = float(np.linalg.norm(points[-1] - points[0]))
    return points, distance


def animate_walk(points: np.ndarray, interval: int = INTERVAL) -> FuncAnimation:
    figure, axes = plt.subplots()
    axes.set_aspect("equal")
    (line,) = axes.plot([], [], "-")
    (start,) = axes.plot([], [], "go")
    (end,) = axes.plot([], [], "ro")

    def update(frame: int) -> tuple:
        path = points[: frame + 1]
        line.set_data(path[:, 0], path[:, 1])
        start.set_data([path[0, 0]], [path[0, 1]])
        end.set_data([path[-1, 0]], [path[-1, 1]])
        return line, start, end

    return FuncAnimation(figure, update, frames=len(points), interval=interval, blit=True)


def main() -> None:
    points, _ = random_walk(STEPS, random.Random())
    animate_walk(points)
    plt.show()


if __name__ == "__main__":
    main()
