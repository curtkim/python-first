# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *

app = QApplication([])
window = QWidget()
window.setFixedWidth(500)

layout = QVBoxLayout()
layout.setContentsMargins(50, 50, 50, 50)
#layout.setSpacing(50)

label1 = QLabel('출발지: ')
label2 = QLabel('도착지: ')

layout.addWidget(label1)
layout.addWidget(label2)

waitingFrame = QFrame()
waitingFrame.setFixedHeight(100)


pickupFrame = QFrame()
pickupFrame.setFixedHeight(100)
pickupButtons = QHBoxLayout()
buttonPickup = QPushButton('승객탑승')
buttonNoshow = QPushButton('noshow')
pickupButtons.addWidget(buttonPickup)
pickupButtons.addWidget(buttonNoshow)
pickupFrame.setLayout(pickupButtons)

drivingFrame = QFrame()
drivingFrame.setFixedHeight(100)
drivingButtons = QHBoxLayout()
buttonComplete = QPushButton('운행완료')
buttonTerminate = QPushButton('승객신고')
drivingButtons.addWidget(buttonComplete)
drivingButtons.addWidget(buttonTerminate)
drivingFrame.setLayout(drivingButtons)

layout.addWidget(waitingFrame)
layout.addWidget(pickupFrame)
#pickupFrame.hide()
layout.addWidget(drivingFrame)
#drivingFrame.hide()

window.setLayout(layout)
window.show()

app.exec_()
