import sys

import rx
from rx import operators as ops
from rx.subject import Subject
from rx.scheduler.mainloop import QtScheduler

try:
    from PyQt5 import QtCore
    from PyQt5.QtWidgets import QApplication, QWidget, QLabel
except ImportError:
    raise ImportError('Please ensure either PySide2 or PyQt5 is available!')


class Window(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Rx for Python rocks")
        self.resize(600, 600)
        self.setMouseTracking(True)

        # This Subject is used to transmit mouse moves to labels
        self.mousemove = Subject()

    def mouseMoveEvent(self, event):
        self.mousemove.on_next((event.x(), event.y()))


def main():
    app = QApplication(sys.argv)
    scheduler = QtScheduler(QtCore)

    window = Window()
    window.show()

    text = 'TIME FLIES LIKE AN ARROW'

    def on_next(info):
        label, (x, y), i = info
        label.move(x + i*15 + 15, y)
        label.show()

    def handle_label(label, i):
        return window.mousemove.pipe(
            ops.delay(i * 0.050),
            ops.map(lambda xy: (label, xy, i)),
            )

    rx.from_(text).pipe(
        ops.map(lambda c: QLabel(c, window)),
        ops.flat_map_indexed(handle_label),
    ).subscribe(on_next, on_error=print, scheduler=scheduler)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()