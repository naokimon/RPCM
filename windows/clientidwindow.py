import json
import requests
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QPixmap, QIcon, QRegularExpressionValidator
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton
from utils import resource_path, load_data, save_data, get_stylesheet


class ClientIdWindow(QMainWindow):
    def __init__(self, main):
        super().__init__()

        self.main_window = main

        self.running = QPixmap(resource_path("./src/images/check.png"))
        self.stopped = QPixmap(resource_path("./src/images/close.png"))
        self.loading = QPixmap(resource_path("./src/images/loading.png"))

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

        self.status_img = self.stopped
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

        data = load_data()

        if not data.get("theme"):
            data["theme"] = "dark"
            save_data(data)

        theme_name = data["theme"]

        with open(resource_path("./data/themes.json"), encoding="utf-8") as f:
            themes = json.load(f)

        theme = themes[theme_name]

        self.setStyleSheet(get_stylesheet(theme))

    def validate(self):
        url = f"https://discord.com/api/v10/applications/{self.input.text()}/rpc"

        response = requests.get(url)

        if response.status_code == 200:
            self.status.setPixmap(self.running)
            data = load_data()
            data["client_id"] = self.input.text()
            save_data(data)
            self.main_window.client_id.setText(self.input.text())
        else:
            self.status.setPixmap(self.stopped)
            self.error_text.setText("Invalid client ID!")