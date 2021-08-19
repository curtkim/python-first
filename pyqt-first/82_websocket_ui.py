# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from threading import Thread
import websocket

try:
    import thread
except ImportError:
    import _thread as thread


# multithread환경에서 문제가 되지 않는 이유는 Python GIL(Global Interpreter Lock) 때문인것 같다.
global ws
new_messages = []


def on_message(ws, message):
    print('on_message', message)
    new_messages.append(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("### opened ###")



#websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://localhost:8080/echo",
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

def run_websocket():
    ws.run_forever()


def main():
    ws_thread = Thread(target=run_websocket) #, daemon=True
    ws_thread.start()

    # GUI:
    app = QApplication([])

    text_area = QPlainTextEdit()
    text_area.setFocusPolicy(Qt.NoFocus)
    message = QLineEdit()

    layout = QVBoxLayout()
    layout.addWidget(text_area)
    layout.addWidget(message)

    window = QWidget()
    window.setLayout(layout)
    window.show()

    def display_new_messages():
        while new_messages:
            text_area.appendPlainText(new_messages.pop(0))

    def send_message():
        ws.send(message.text())
        message.clear()

    # Signals:
    message.returnPressed.connect(send_message)

    timer = QTimer()
    timer.timeout.connect(display_new_messages)
    timer.start(100)

    app.exec_()
    # ui가 닫히면 websocket도 닫는다.
    ws.close()


if __name__ == '__main__':
    main()
