import pytest

from python_tasks.s01_basics.t04_fibonacci import main, nth_fibonacci

EXPECTED_1000TH = (
    "2686381002448535938614672720214292396761660931898695234012317599761798"
    "1700247881689338369654483356564191827856161443356312976673642210350324"
    "634850410377680367334151172899169723197082763985615764450078474174626"
)


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        pytest.param(1, 0, id="first"),
        pytest.param(2, 1, id="second"),
        pytest.param(3, 1, id="third"),
        pytest.param(4, 2, id="fourth"),
        pytest.param(5, 3, id="fifth"),
        pytest.param(6, 5, id="sixth"),
        pytest.param(7, 8, id="seventh"),
        pytest.param(8, 13, id="eighth"),
        pytest.param(9, 21, id="ninth"),
        pytest.param(10, 34, id="tenth"),
        pytest.param(20, 4181, id="twentieth"),
    ],
)
def test_nth_fibonacci(n: int, expected: int) -> None:
    assert nth_fibonacci(n) == expected


def test_thousandth_term_matches_reference_value() -> None:
    value = nth_fibonacci(1000)
    assert str(value) == EXPECTED_1000TH
    assert len(str(value)) == 209


@pytest.mark.parametrize("n", range(3, 201))
def test_nth_fibonacci_recurrence(n: int) -> None:
    assert nth_fibonacci(n) == nth_fibonacci(n - 1) + nth_fibonacci(n - 2)


@pytest.mark.parametrize(
    "n",
    [
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
        pytest.param(-100, id="large-negative"),
    ],
)
def test_nth_fibonacci_rejects_invalid_indexes(n: int) -> None:
    with pytest.raises(ValueError):
        nth_fibonacci(n)


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(True, id="bool-true"),
        pytest.param(False, id="bool-false"),
        pytest.param(1.0, id="float"),
        pytest.param("1", id="string"),
        pytest.param(None, id="none"),
    ],
)
def test_nth_fibonacci_rejects_wrong_types(value: object) -> None:
    with pytest.raises(TypeError):
        nth_fibonacci(value)


def test_cli_output(run_cli) -> None:
    code, out, err = run_cli(main, "")
    assert code is None
    assert out.strip() == EXPECTED_1000TH
    assert err == ""
