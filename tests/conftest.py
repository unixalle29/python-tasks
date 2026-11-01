import io
import os
from collections.abc import Callable

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("MPLBACKEND", "Agg")


@pytest.fixture
def run_cli(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> Callable[[Callable[[], None], str], tuple[object | None, str, str]]:
    def run(function: Callable[[], None], stdin: str) -> tuple[object | None, str, str]:
        monkeypatch.setattr("sys.stdin", io.StringIO(stdin))
        code: object | None = None
        try:
            function()
        except SystemExit as exc:
            code = exc.code
        captured = capsys.readouterr()
        return code, captured.out, captured.err

    return run


@pytest.fixture
def assert_cli_error(run_cli) -> Callable[[Callable[[], None], str], None]:
    def check(function: Callable[[], None], stdin: str) -> None:
        code, out, err = run_cli(function, stdin)
        assert code == 2
        assert out == ""
        assert err.startswith("error:")

    return check
