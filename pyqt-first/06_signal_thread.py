import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSignal
from time import sleep


class Main(QWidget):

    def __init__(self):
        super().__init__()

    def StartButtonEvent(self):
        self.test = ExecuteThread()
        self.test.start()
        self.test.finished.connect(self.thread_finished)
        self.test.my_signal.connect(self.my_event)

    def thread_finished(self):
        # gets executed if thread finished
        pass

    def my_event(self):
        # gets executed on my_signal
        pass


class ExecuteThread(QThread):
    my_signal = pyqtSignal()

    def run(self):
        # do something here
        sleep(1)
        self.my_signal.emit()
        pass


def main(argv):
    app = QApplication(argv)
    window = Main()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main(sys.argv)
