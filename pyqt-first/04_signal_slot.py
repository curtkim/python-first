from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

app = QApplication([])
button = QPushButton('클릭')

# font: QFont = button.font()
# font.setPointSize(25)
# button.setFont(font)

button.setStyleSheet("font-size: 100px;")
#button.setFont(QFont('Times', 25))

def on_button_clicked():
    alert = QMessageBox()
    alert.setText('You clicked the button!')
    alert.exec_()

button.clicked.connect(on_button_clicked)
button.show()
app.exec_()

# windows가 닫히고 실행된다.
print('end')
