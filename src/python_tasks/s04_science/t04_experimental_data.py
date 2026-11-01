import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

REQUIRED_ARGUMENTS = 2
MIN_COLUMNS = 2


def read_measurements(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = [float(value) for value in line.split()]
        except ValueError as exc:
            raise ValueError(f"invalid number in line: {line}") from exc
        if len(row) < MIN_COLUMNS:
            raise ValueError("each line needs x and at least one measurement")
        rows.append(row)
    if not rows:
        raise ValueError("file is empty")
    if not all(np.isfinite(values).all() for values in rows):
        raise ValueError("all values must be finite")
    x = np.array([row[0] for row in rows])
    measurements = [row[1:] for row in rows]
    means = np.array([sum(values) / len(values) for values in measurements])
    errors = np.array([np.std(values) for values in measurements])
    return x, means, errors


def plot_measurements(x: np.ndarray, means: np.ndarray, errors: np.ndarray) -> None:
    _, axes = plt.subplots()
    axes.errorbar(x, means, yerr=errors, fmt="o-", capsize=3)
    axes.set_xlabel("x")
    axes.set_ylabel("mean value")


def main() -> None:
    if len(sys.argv) != REQUIRED_ARGUMENTS:
        print("usage: python -m ... FILE", file=sys.stderr)
        raise SystemExit(2)
    try:
        x, means, errors = read_measurements(Path(sys.argv[1]))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    plot_measurements(x, means, errors)
    plt.show()


if __name__ == "__main__":
    main()
