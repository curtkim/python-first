import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class signal_test(QObject):
    signal1 = pyqtSignal()

    def run(self):
        self.signal1.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        mainsignal = signal_test()
        mainsignal.signal1.connect(self.signal1_emit)
        mainsignal.run()

    @pyqtSlot()
    def signal1_emit(self):
        print("signal test")


def main(argv):
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main(sys.argv)
