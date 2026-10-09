from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSharedMemory
import sys
from gui import MainWindow

def main():
    app = QApplication(sys.argv)

    shared_mem = QSharedMemory("RPCM_SINGLE_INSTANCE")

    window = MainWindow()

    if not shared_mem.create(1):
        return 0

    window.resize(1080, 720)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())