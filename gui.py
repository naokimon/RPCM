import json
from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QLabel, QToolButton, QFrame, QCheckBox
from PySide6.QtGui import QIcon, QPixmap, QRegularExpressionValidator
import webbrowser
from rpc import PresenceThread
from schemas import RPCDataModel
import requests
from utils import load_data, save_data, resource_path


class ClientIdWindow(QMainWindow):
    def __init__(self, main):
        super().__init__()

        self.main_window: MainWindow = main

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.running = QPixmap(resource_path("./src/images/check.png"))
        self.stopped = QPixmap(resource_path("./src/images/close.png"))
        self.loading = QPixmap(resource_path("./src/images/loading.png"))

        self.setWindowTitle("RPCM")
        icon_path = str(resource_path("./src/images/RPCM.png"))
        self.setWindowIcon(QIcon(icon_path))

        self.thread = None

        container = QWidget()
        self.setCentralWidget(container)

        layout = QVBoxLayout(container)
        form = QFormLayout()

        regex = QRegularExpression(r"^[1-9]\d*$")
        int_validator = QRegularExpressionValidator(regex)

        self.client_id_window = ClientIdWindow(self)

        self.client_btn = QPushButton("Set Client ID")
        self.client_btn.clicked.connect(self.show_client_id)

        self.dev_btn = QPushButton("Go to Developer Portal")
        self.dev_btn.clicked.connect(
            lambda: webbrowser.open("https://discord.com/developers/home")
        )

        data = load_data()
        self.client_id = QLabel(str(data.get("client_id")))

        data = load_data()
        rcp = data.get("recent") or {}

        self.name = QLineEdit(rcp.get("name", ""))
        self.state = QLineEdit(rcp.get("state", ""))
        self.details = QLineEdit(rcp.get("details", ""))

        form.addRow("Client ID:", self.client_id)
        form.addRow("Name:", self.name)
        form.addRow("State:", self.state)
        form.addRow("Details:", self.details)

        self.large_image = QLineEdit(rcp.get("large_image", ""))
        form.addRow("Large image:", self.large_image)
        self.large_text = QLineEdit(rcp.get("large_text", ""))
        form.addRow("Large text:", self.large_text)

        self.small_image = QLineEdit(rcp.get("small_image", ""))
        form.addRow("Small image:", self.small_image)
        self.small_text = QLineEdit(rcp.get("small_text", ""))
        form.addRow("Small text:", self.small_text)

        self.start = QLineEdit(str(rcp.get("start") or ""))
        self.start.setValidator(int_validator)

        self.end = QLineEdit(str(rcp.get("end") or ""))
        self.end.setValidator(int_validator)

        form.addRow("Start:", self.start)
        form.addRow("End:", self.end)

        self.advanced_layout = QVBoxLayout()

        self.advanced_btn = QToolButton()
        self.advanced_btn.setText("Advanced options")
        self.advanced_btn.setCheckable(True)
        self.advanced_btn.setChecked(False)
        self.advanced_btn.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextBesideIcon
        )
        self.advanced_btn.setArrowType(Qt.ArrowType.RightArrow)

        self.advanced_btn.setStyleSheet("""
            QToolButton {
                border: none;
                text-align: left;
            }
            QToolButton:hover {
                color: #d6d6d6;
            }
        """)

        self.advanced_btn.clicked.connect(self.toggle_advanced)

        self.advanced_container = QFrame()
        self.advanced_container.setVisible(False)

        self.advanced_options = QFormLayout(self.advanced_container)

        self.button_label = QLabel("Buttons:")
        self.button_row = QHBoxLayout()

        self.btn1_text = QLineEdit()
        self.btn1_url = QLineEdit()

        self.btn1_col = QFormLayout()
        self.btn1_col.addRow("Text:", self.btn1_text)
        self.btn1_col.addRow("URL:", self.btn1_url)

        self.btn2_text = QLineEdit()
        self.btn2_url = QLineEdit()

        self.btn2_col = QFormLayout()
        self.btn2_col.addRow("Text:", self.btn2_text)
        self.btn2_col.addRow("URL:", self.btn2_url)

        self.button_row.addLayout(self.btn1_col)
        self.button_row.addLayout(self.btn2_col)

        self.advanced_options.addRow(self.button_label)
        self.advanced_options.addRow(self.button_row)

        self.state_url = QLineEdit(rcp.get("state_url"))
        self.details_url = QLineEdit(rcp.get("details_url"))
        self.large_url = QLineEdit(rcp.get("large_url"))
        self.small_url = QLineEdit(rcp.get("small_url"))

        self.advanced_options.addRow("State URL:", self.state_url)
        self.advanced_options.addRow("Details URL:", self.details_url)
        self.advanced_options.addRow("Large Image URL:", self.large_url)
        self.advanced_options.addRow("Small Image URL:", self.small_url)

        self.instance = QCheckBox()
        self.instance.setChecked(True) if rcp.get("instance") is True else self.instance.setChecked(False)
        self.advanced_options.addRow("Instance:", self.instance)

        self.advanced_layout.addWidget(self.advanced_btn)
        self.advanced_layout.addWidget(self.advanced_container)

        run_row = QHBoxLayout()

        self.run_btn = QPushButton("Run")
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)

        self.run_btn.clicked.connect(self.run)
        self.stop_btn.clicked.connect(self.stop)

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
        layout.addWidget(self.dev_btn)
        layout.addLayout(form)
        layout.addLayout(self.advanced_layout)
        layout.addStretch()
        layout.addLayout(bottom_layout)

    def toggle_advanced(self, checked):
        self.advanced_container.setVisible(True) if not self.advanced_container.isVisible() \
        else self.advanced_container.setVisible(False)

        self.advanced_btn.setArrowType(
            Qt.ArrowType.DownArrow if checked else Qt.ArrowType.RightArrow
        )

    def show_client_id(self):
        self.client_id_window.show()

    def run(self):
        client_id = self.client_id.text().strip()

        if not client_id.isdigit():
            self.error_text.setText("Invalid client ID!")
            return

        buttons = []

        for text_field, url_field in [
            (self.btn1_text, self.btn1_url),
            (self.btn2_text, self.btn2_url),
        ]:
            if text_field.text() and url_field.text():
                buttons.append({
                    "label": text_field.text(),
                    "url": url_field.text()
                })

        print(buttons)

        rpc_data = {
            "name": self.name.text().strip() or None,
            "state": self.state.text().strip() or None,
            "details": self.details.text().strip() or None,
            "large_image": self.large_image.text().strip() or None,
            "large_text": self.large_text.text().strip() or None,
            "small_image": self.small_image.text().strip() or None,
            "small_text": self.small_text.text().strip() or None,
            "buttons": buttons,
            "start": int(self.start.text()) if self.start.text() else None,
            "end": int(self.end.text()) if self.end.text() else None,
            "state_url": self.state_url.text() or None,
            "details_url": self.details_url.text() or None,
            "large_url": self.large_url.text() or None,
            "small_url": self.small_url.text() or None,
            "instance": self.instance.isChecked()
        }

        try:
            validated_data = RPCDataModel.model_validate(rpc_data)
            data = load_data()
            data["recent"] = rpc_data
            save_data(data)
        except Exception as e:
            self.error_text.setText(str(e))
            return

        self.thread = PresenceThread(validated_data)

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