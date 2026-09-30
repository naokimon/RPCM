from PySide6.QtWidgets import QApplication
from schemas import RPCDataModel
from gui import MainWindow

app = QApplication()

window = MainWindow()
window.show()
window.resize(1080, 720)

app.exec()

