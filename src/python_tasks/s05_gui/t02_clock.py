import sys
from datetime import UTC, datetime

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QLabel


def format_time(now: datetime) -> str:
    return now.strftime("%H:%M:%S\n%d.%m.%Y")


class DigitalClock(QLabel):
    def __init__(self) -> None:
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("font-size: 32px;")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self) -> None:
        self.setText(format_time(datetime.now(tz=UTC).astimezone()))


def main() -> None:
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
