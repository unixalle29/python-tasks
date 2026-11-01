from pathlib import Path

from PyQt6.QtGui import QColor, QImage, QPixmap

from python_tasks.s05_gui.t04_image_viewer import ImageViewer, rotate_pixmap


def make_pixmap(width: int, height: int) -> QPixmap:
    image = QImage(width, height, QImage.Format.Format_RGB32)
    image.fill(QColor("red"))
    return QPixmap.fromImage(image)


def test_rotate_90_swaps_dimensions(qapp) -> None:
    pixmap = rotate_pixmap(make_pixmap(2, 1), 90)
    assert (pixmap.width(), pixmap.height()) == (1, 2)


def test_rotate_180_keeps_dimensions(qapp) -> None:
    pixmap = rotate_pixmap(make_pixmap(2, 1), 180)
    assert (pixmap.width(), pixmap.height()) == (2, 1)


def test_viewer_opens_and_rotates_image(qtbot, tmp_path: Path) -> None:
    path = tmp_path / "image.png"
    assert make_pixmap(2, 1).save(str(path), "PNG")
    viewer = ImageViewer()
    qtbot.addWidget(viewer)
    viewer.open_image(path)
    viewer.rotate(90)
    assert viewer.pixmap is not None
    assert (viewer.pixmap.width(), viewer.pixmap.height()) == (1, 2)
