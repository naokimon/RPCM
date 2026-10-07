import json
from PySide6.QtCore import QRegularExpression, QThread
from PySide6.QtWidgets import QMainWindow, QWidget, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QIcon, QPixmap, QRegularExpressionValidator
import webbrowser
from rpc import PresenceThread
from schemas import RPCDataModel
import requests
from utils import client_id_exists, resource_path


class ClientIdWindow(QMainWindow):
    def __init__(self, main):
        super().__init__()

        self.main_window: MainWindow = main

        self.setWindowTitle("RPCM")
        self.setWindowIcon(QIcon(str(resource_path("src/images/RPCM.ico"))))

        container = QWidget()
        self.setCentralWidget(container)

        layout = QVBoxLayout(container)

        self.description = QLabel("Client ID:")

        regex = QRegularExpression(r"^-?\d*$")
        int_validator = QRegularExpressionValidator(regex)

        self.input = QLineEdit()
        self.input.setValidator(int_validator)


        self.error_text = QLabel()
        self.error_text.setStyleSheet("color: #FF0000;")

        self.validate_row = QHBoxLayout()

        self.status_img = QPixmap("./src/images/close.png")
        self.status = QLabel()
        self.status.setScaledContents(True)
        self.status.setFixedSize(20, 20)
        self.status.setPixmap(self.status_img)

        self.validate_btn = QPushButton("Validate")
        self.validate_btn.clicked.connect(self.validate)

        self.validate_row.addWidget(self.validate_btn)
        self.validate_row.addWidget(self.status)

        layout.addWidget(self.description)
        layout.addWidget(self.input)
        layout.addWidget(self.error_text)
        layout.addLayout(self.validate_row)

    def validate(self):
        url = f"https://discord.com/api/v10/applications/{self.input.text()}/rpc"

        response = requests.get(url)

        if response.status_code == 200:
            self.status.setPixmap(QPixmap("./src/images/check.png"))
            client_id_exists()
            with open("data/client_id.json", "w") as f:
                json.dump({
                    "client_id": self.input.text()
                }, f)
            self.main_window.client_id.setText(self.input.text())
        else:
            self.error_text.setText("Invalid client ID!")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RPCM")
        self.setWindowIcon(QIcon("src/images/RPCM.png"))

        self.thread = None

        container = QWidget()
        self.setCentralWidget(container)

        layout = QVBoxLayout(container)
        form = QFormLayout()

        regex = QRegularExpression(r"^-?\d*$")
        int_validator = QRegularExpressionValidator(regex)

        self.client_id_window = ClientIdWindow(self)

        self.client_btn = QPushButton("Set Client ID")
        self.client_btn.clicked.connect(self.show_client_id)

        self.image_btn = QPushButton("Go to Developer Portal")
        self.image_btn.clicked.connect(
            lambda: webbrowser.open("https://discord.com/developers/home")
        )

        client_id_exists()
        with open("data/client_id.json") as f:
            data = json.load(f)

        self.client_id = QLabel(str(data.get("client_id")) or None)
        self.name = QLineEdit()
        self.state = QLineEdit()
        self.details = QLineEdit()

        form.addRow("Client ID:", self.client_id)
        form.addRow("Name:", self.name)
        form.addRow("State:", self.state)
        form.addRow("Details:", self.details)

        self.large_image = QLineEdit()
        form.addRow("Large image:", self.large_image)
        self.large_text = QLineEdit()
        form.addRow("Large text:", self.large_text)

        self.small_image = QLineEdit()
        form.addRow("Small image:", self.small_image)
        self.small_text = QLineEdit()
        form.addRow("Small text:", self.small_text)

        self.start = QLineEdit()
        self.start.setValidator(int_validator)

        self.end = QLineEdit()
        self.end.setValidator(int_validator)

        form.addRow("Start:", self.start)
        form.addRow("End:", self.end)

        run_row = QHBoxLayout()

        self.run_btn = QPushButton("Run")
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)

        self.run_btn.clicked.connect(self.run)
        self.stop_btn.clicked.connect(self.stop)

        self.running = QPixmap(resource_path("./src/images/check.png"))
        self.stopped = QPixmap(resource_path("./src/images/close.png"))
        self.loading = QPixmap(resource_path("./src/images/loading.png"))
        self.status = QLabel()
        self.status.setPixmap(self.stopped)
        self.status.setScaledContents(True)
        self.status.setFixedSize(25, 25)

        buttons_col = QVBoxLayout()
        buttons_col.addWidget(self.run_btn)
        buttons_col.addWidget(self.stop_btn)

        run_row.addLayout(buttons_col)
        run_row.addWidget(self.status)

        self.error_row = QHBoxLayout()
        self.error_text = QLabel()
        self.error_text.setStyleSheet("color: #FF0000;")
        self.error_row.addWidget(self.error_text)

        bottom_layout = QVBoxLayout()
        bottom_layout.addLayout(self.error_row)
        bottom_layout.addLayout(run_row)
        bottom_layout.addSpacing(2)

        layout.addWidget(self.client_btn)
        layout.addWidget(self.image_btn)
        layout.addLayout(form)
        layout.addStretch()
        layout.addLayout(bottom_layout)

    def show_client_id(self):
        self.client_id_window.show()

    def run(self):
        client_id = self.client_id.text().strip()

        if not client_id.isdigit():
            self.error_text.setText("Invalid client ID!")
            return

        data = {
            "name": self.name.text().strip() or None,
            "state": self.state.text().strip() or None,
            "details": self.details.text().strip() or None,
            "large_image": self.large_image.text().strip() or None,
            "large_text": self.large_text.text().strip() or None,
            "small_image": self.small_image.text().strip() or None,
            "small_text": self.small_text.text().strip() or None,
            "start": int(self.start.text()) if self.start.text() else None,
            "end": int(self.end.text()) if self.end.text() else None,
        }

        try:
            rpc_data = RPCDataModel.model_validate(data)
        except Exception as e:
            self.error_text.setText(str(e))
            return

        self.thread = PresenceThread(rpc_data)

        self.thread.connected.connect(self.on_rpc_connected)
        self.thread.finished.connect(self.on_thread_finished)
        self.thread.error.connect(self.on_thread_error)

        self.thread.start()

        self.run_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.status.setPixmap(self.loading)

    def stop(self):
        if self.thread and self.thread.isRunning():
            self.status.setPixmap(self.loading)
            self.thread.stop()
            self.stop_btn.setEnabled(False)

    def on_thread_finished(self):
        self.status.setPixmap(self.stopped)
        self.stop_btn.setEnabled(False)
        self.run_btn.setEnabled(True)

        if self.thread is not None:
            self.thread.deleteLater()
            self.thread = None

    def on_thread_error(self, message):
        self.error_text.setText(message)

    def on_rpc_connected(self):
        self.stop_btn.setEnabled(True)
        self.status.setPixmap(self.running)