import pytest

from python_tasks.s02_data.t01_palindrome import is_palindrome, main, parse_text, reverse_text


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        pytest.param("hello", "hello", id="plain"),
        pytest.param("  hello  ", "hello", id="surrounding-whitespace"),
        pytest.param("123", "123", id="digits"),
        pytest.param("Я", "Я", id="single-letter"),
    ],
)
def test_parse_text_valid(raw: str, expected: str) -> None:
    assert parse_text(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        pytest.param("", id="empty"),
        pytest.param("   ", id="spaces"),
        pytest.param("\n\t", id="whitespace"),
        pytest.param(".,!?", id="punctuation"),
    ],
)
def test_parse_text_rejects_invalid_input(raw: str) -> None:
    with pytest.raises(ValueError):
        parse_text(raw)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        pytest.param("abc", "cba", id="ascii"),
        pytest.param("Коту тащат уток", "коту тащат утоК", id="russian"),
        pytest.param("12321", "12321", id="digits"),
        pytest.param("", "", id="empty"),
    ],
)
def test_reverse_text(text: str, expected: str) -> None:
    assert reverse_text(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        pytest.param("Коту тащат уток", True, id="russian-phrase"),
        pytest.param("А роза упала на лапу Азора", True, id="classic-phrase"),
        pytest.param("Я", True, id="single-letter"),
        pytest.param("12321", True, id="digits"),
        pytest.param("АББА", True, id="case-insensitive"),
        pytest.param("привет", False, id="non-palindrome"),
        pytest.param("абв", False, id="russian-non-palindrome"),
        pytest.param("", True, id="empty"),
    ],
)
def test_is_palindrome(text: str, expected: bool) -> None:
    assert is_palindrome(text) is expected


@pytest.mark.parametrize(
    ("stdin", "expected"),
    [
        pytest.param("Коту тащат уток\n", "коту тащат утоК\nyes", id="palindrome"),
        pytest.param("абв\n", "вба\nno", id="non-palindrome"),
        pytest.param("12321\n", "12321\nyes", id="digits"),
    ],
)
def test_cli_output(run_cli, stdin: str, expected: str) -> None:
    code, out, err = run_cli(main, stdin)
    assert code is None
    assert out.strip() == expected
    assert err == ""


@pytest.mark.parametrize(
    "stdin",
    [
        pytest.param("", id="empty"),
        pytest.param("   \n", id="spaces"),
        pytest.param(".,!?\n", id="punctuation"),
    ],
)
def test_cli_rejects_invalid_input(assert_cli_error, stdin: str) -> None:
    assert_cli_error(main, stdin)
