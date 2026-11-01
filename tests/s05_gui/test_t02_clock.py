from datetime import datetime

from python_tasks.s05_gui.t02_clock import DigitalClock, format_time


def test_format_time() -> None:
    assert format_time(datetime(2024, 5, 6, 7, 8, 9)) == "07:08:09\n06.05.2024"


def test_clock_shows_time_and_date(qtbot) -> None:
    clock = DigitalClock()
    qtbot.addWidget(clock)
    assert clock.timer.isActive()
    assert len(clock.text().splitlines()) == 2
    clock.update_time()
