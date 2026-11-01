import pytest

from python_tasks.s02_data.t05_scores import EGE_SCORES, main, students_above_average

EXPECTED_ABOVE_AVERAGE = ["Крутой", "Лебеденко", "Смирнов", "Петрова", "Симчук"]


def test_students_above_average_for_ege_scores() -> None:
    assert students_above_average(EGE_SCORES) == EXPECTED_ABOVE_AVERAGE


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        pytest.param({"A": 1, "B": 2, "C": 3}, ["C"], id="one-above"),
        pytest.param({"A": 1, "B": 1}, [], id="all-equal"),
        pytest.param({"A": 0, "B": 0, "C": 0}, [], id="all-zero"),
        pytest.param({"A": 0, "B": 3, "C": 3, "D": 0}, ["B", "C"], id="tie-above"),
        pytest.param({"A": 1, "B": 2}, ["B"], id="above-average"),
    ],
)
def test_students_above_average(scores: dict[str, int], expected: list[str]) -> None:
    assert students_above_average(scores) == expected


def test_students_above_average_rejects_empty_scores() -> None:
    with pytest.raises(ValueError):
        students_above_average({})


@pytest.mark.parametrize(
    "scores",
    [
        pytest.param({"A": -1, "B": 2}, id="one-negative"),
        pytest.param({"A": -10, "B": -1}, id="all-negative"),
    ],
)
def test_students_above_average_rejects_negative_scores(scores: dict[str, int]) -> None:
    with pytest.raises(ValueError):
        students_above_average(scores)


@pytest.mark.parametrize(
    "scores",
    [
        pytest.param({"A": True, "B": 2}, id="bool"),
        pytest.param({"A": 1.5, "B": 2}, id="float"),
        pytest.param({"A": "1", "B": 2}, id="string"),
        pytest.param({"A": None, "B": 2}, id="none"),
    ],
)
def test_students_above_average_rejects_wrong_types(scores: dict[str, object]) -> None:
    with pytest.raises(TypeError):
        students_above_average(scores)


def test_cli_output(run_cli) -> None:
    code, out, err = run_cli(main, "")
    assert code is None
    assert err == ""
    assert out.strip().splitlines() == EXPECTED_ABOVE_AVERAGE
