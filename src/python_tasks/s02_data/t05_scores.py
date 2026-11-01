from collections.abc import Mapping

EGE_SCORES: dict[str, int] = {
    "Андреев": 62,
    "Степанов": 45,
    "Крутой": 93,
    "Лебеденко": 88,
    "Смирнов": 98,
    "Петрова": 83,
    "Симчук": 75,
    "Лихая": 71,
    "Неизвестный": 39,
}


def _validate_scores(scores: Mapping[str, int]) -> None:
    if not scores:
        raise ValueError("scores must not be empty")
    if any(isinstance(score, bool) or not isinstance(score, int) for score in scores.values()):
        raise TypeError("scores must be integers")
    if any(score < 0 for score in scores.values()):
        raise ValueError("scores must be non-negative")


def students_above_average(scores: Mapping[str, int]) -> list[str]:
    _validate_scores(scores)
    average = sum(scores.values()) / len(scores)
    return [name for name, score in scores.items() if score > average]


def main() -> None:
    for name in students_above_average(EGE_SCORES):
        print(name)


if __name__ == "__main__":
    main()
