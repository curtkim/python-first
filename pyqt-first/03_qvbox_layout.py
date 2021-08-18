from PyQt5.QtWidgets import *

app = QApplication([])
window = QWidget()

layout = QVBoxLayout()
layout.setContentsMargins(50, 50, 50, 50)
layout.setSpacing(100)
layout.addWidget(QPushButton('Top'))
layout.addWidget(QPushButton('Bottom'))

window.setLayout(layout)
window.show()

app.exec_()