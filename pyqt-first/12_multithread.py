from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from requests import Session
from threading import Thread
import threading
from time import sleep

print('main', threading.get_ident())

name = input("Please enter your name: ")
chat_url = "https://build-system.fman.io/chat"
server = Session()

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

# Event handlers:
new_messages = []
def fetch_new_messages():
    while True:
        response = server.get(chat_url).text
        if response:
            print('fetch_new_messages', threading.get_ident())
            new_messages.append(response)
        sleep(.5)

thread = Thread(target=fetch_new_messages, daemon=True)
thread.start()



def display_new_messages():
    print('display_new_messages', threading.get_ident())
    while new_messages:
        text_area.appendPlainText(new_messages.pop(0))


def send_message():
    print('send_message', threading.get_ident())
    server.post(chat_url, {"name": name, "message": message.text()})
    message.clear()

# Signals:
message.returnPressed.connect(send_message)

# timer
# display_new_messages는 main thread에서 실행된다.
timer = QTimer()
timer.timeout.connect(display_new_messages)
timer.start(2000)

app.exec_()
