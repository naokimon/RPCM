import json
import webbrowser
from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QPixmap, QIcon, QRegularExpressionValidator
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFormLayout, QPushButton, QLabel, QLineEdit, QToolButton, QFrame, QComboBox, QHBoxLayout, QCheckBox, QScrollArea, QSizePolicy
from windows.clientidwindow import ClientIdWindow
from pypresence import ActivityType, StatusDisplayType
from rpc import PresenceThread
from schemas import RPCDataModel
from utils import resource_path, load_data, save_data, get_stylesheet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.running = QPixmap(resource_path("./src/images/check.png"))
        self.stopped = QPixmap(resource_path("./src/images/close.png"))
        self.loading = QPixmap(resource_path("./src/images/loading.png"))

        self.setWindowTitle("RPCM")
        self.setMinimumSize(500, 680)
        self.resize(560, 760)

        icon_path = str(resource_path("./src/images/RPCM.png"))
        self.setWindowIcon(QIcon(icon_path))

        self.thread = None

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.container = QWidget()
        self.container.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Minimum,
        )

        self.scroll_area.setWidget(self.container)
        self.setCentralWidget(self.scroll_area)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(12)
        layout.setSizeConstraint(
            QVBoxLayout.SizeConstraint.SetMinimumSize
        )

        form = QFormLayout()
        form.setContentsMargins(0, 8, 0, 8)
        form.setHorizontalSpacing(16)
        form.setVerticalSpacing(11)
        form.setLabelAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        form.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow
        )

        regex = QRegularExpression(r"^[1-9]\d*$")
        int_validator = QRegularExpressionValidator(regex)

        self.client_id_window = ClientIdWindow(self)

        self.client_btn = QPushButton("Set Client ID")
        self.client_btn.setObjectName("secondaryButton")
        self.client_btn.clicked.connect(self.show_client_id)

        self.dev_btn = QPushButton("Open Developer Portal  ↗")
        self.dev_btn.setObjectName("secondaryButton")
        self.dev_btn.clicked.connect(
            lambda: webbrowser.open(
                "https://discord.com/developers/home"
            )
        )

        data = load_data()
        self.client_id = QLabel(str(data.get("client_id") or ""))
        self.client_id.setObjectName("clientIdValue")
        self.client_id.setWordWrap(True)
        self.client_id.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        rpc = data.get("recent") or {}

        self.name = QLineEdit(rpc.get("name") or "")
        self.state = QLineEdit(rpc.get("state") or "")
        self.details = QLineEdit(rpc.get("details") or "")

        form.addRow("Client ID:", self.client_id)
        form.addRow("Name:", self.name)
        form.addRow("State:", self.state)
        form.addRow("Details:", self.details)

        self.large_image = QLineEdit(
            rpc.get("large_image") or ""
        )
        form.addRow("Large image:", self.large_image)

        self.large_text = QLineEdit(
            rpc.get("large_text") or ""
        )
        form.addRow("Large text:", self.large_text)

        self.small_image = QLineEdit(
            rpc.get("small_image") or ""
        )
        form.addRow("Small image:", self.small_image)

        self.small_text = QLineEdit(
            rpc.get("small_text") or ""
        )
        form.addRow("Small text:", self.small_text)

        self.start = QLineEdit(str(rpc.get("start") or ""))
        self.start.setValidator(int_validator)
        form.addRow("Start:", self.start)

        self.end = QLineEdit(str(rpc.get("end") or ""))
        self.end.setValidator(int_validator)
        form.addRow("End:", self.end)

        self.advanced_layout = QVBoxLayout()
        self.advanced_layout.setSpacing(8)

        self.advanced_btn = QToolButton()
        self.advanced_btn.setText("Advanced options")
        self.advanced_btn.setCheckable(True)
        self.advanced_btn.setChecked(False)
        self.advanced_btn.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextBesideIcon
        )
        self.advanced_btn.setArrowType(Qt.ArrowType.RightArrow)
        self.advanced_btn.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

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
        self.advanced_container.setObjectName("advancedPanel")
        self.advanced_container.setVisible(False)
        self.advanced_container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Maximum,
        )

        self.advanced_options = QFormLayout(
            self.advanced_container
        )
        self.advanced_options.setContentsMargins(12, 12, 12, 12)
        self.advanced_options.setHorizontalSpacing(12)
        self.advanced_options.setVerticalSpacing(10)
        self.advanced_options.setLabelAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.advanced_options.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow
        )

        self.activity_type = QComboBox()
        self.activity_type.addItems([
            "Playing",
            "Listening",
            "Watching",
            "Competing",
        ])

        self.status_display_type = QComboBox()
        self.status_display_type.addItems([
            "Name",
            "State",
            "Details",
        ])

        self.advanced_options.addRow(
            "Activity types:",
            self.activity_type,
        )
        self.advanced_options.addRow(
            "Status display types:",
            self.status_display_type,
        )

        self.button_label = QLabel("Buttons:")

        self.button_row = QHBoxLayout()
        self.button_row.setSpacing(12)

        self.btn1_text = QLineEdit()
        self.btn1_url = QLineEdit()

        self.btn1_col = QFormLayout()
        self.btn1_col.setVerticalSpacing(8)
        self.btn1_col.addRow("Text:", self.btn1_text)
        self.btn1_col.addRow("URL:", self.btn1_url)

        self.btn2_text = QLineEdit()
        self.btn2_url = QLineEdit()

        self.btn2_col = QFormLayout()
        self.btn2_col.setVerticalSpacing(8)
        self.btn2_col.addRow("Text:", self.btn2_text)
        self.btn2_col.addRow("URL:", self.btn2_url)

        self.button_row.addLayout(self.btn1_col, 1)
        self.button_row.addLayout(self.btn2_col, 1)

        self.advanced_options.addRow(self.button_label)
        self.advanced_options.addRow(self.button_row)

        self.state_url = QLineEdit(rpc.get("state_url") or "")
        self.details_url = QLineEdit(rpc.get("details_url") or "")
        self.large_url = QLineEdit(rpc.get("large_url") or "")
        self.small_url = QLineEdit(rpc.get("small_url") or "")

        self.advanced_options.addRow("State URL:", self.state_url)
        self.advanced_options.addRow("Details URL:", self.details_url)
        self.advanced_options.addRow("Large Image URL:", self.large_url)
        self.advanced_options.addRow("Small Image URL:", self.small_url)

        self.instance = QCheckBox()
        self.instance.setChecked(rpc.get("instance") is True)

        self.advanced_options.addRow("Instance:", self.instance)


        self.advanced_layout.addWidget(self.advanced_btn)
        self.advanced_layout.addWidget(self.advanced_container)

        run_row = QHBoxLayout()
        run_row.setSpacing(12)

        self.run_btn = QPushButton("Start presence")
        self.run_btn.setObjectName("primaryButton")

        self.stop_btn = QPushButton("Stop presence")
        self.stop_btn.setObjectName("dangerButton")
        self.stop_btn.setEnabled(False)

        self.run_btn.clicked.connect(self.run)
        self.stop_btn.clicked.connect(self.stop)

        self.status = QLabel()
        self.status.setObjectName("connectionStatus")
        self.status.setToolTip("Presence connection status")
        self.status.setPixmap(self.stopped)
        self.status.setScaledContents(True)
        self.status.setFixedSize(25, 25)

        buttons_col = QVBoxLayout()
        buttons_col.setSpacing(8)
        buttons_col.addWidget(self.run_btn)
        buttons_col.addWidget(self.stop_btn)

        run_row.addLayout(buttons_col)
        run_row.addWidget(self.status)
        run_row.addStretch(1)

        self.error_row = QHBoxLayout()

        self.error_text = QLabel()
        self.error_text.setObjectName("errorText")
        self.error_text.setWordWrap(True)
        self.error_text.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )

        self.error_row.addWidget(self.error_text)

        bottom_layout = QVBoxLayout()
        bottom_layout.setSpacing(8)
        bottom_layout.addLayout(self.error_row)
        bottom_layout.addLayout(run_row)

        layout.addWidget(self.client_btn)
        layout.addWidget(self.dev_btn)
        layout.addLayout(form)
        layout.addWidget(self._section_divider())
        layout.addLayout(self.advanced_layout)
        layout.addLayout(bottom_layout)

        data = load_data()

        if not data.get("theme"):
            data["theme"] = "dark"
            save_data(data)

        theme_name = data["theme"]

        with open(resource_path("./data/themes.json"), encoding="utf-8",) as f:
            themes = json.load(f)

        theme = themes[theme_name]

        self.setStyleSheet(get_stylesheet(theme))

    @staticmethod
    def _section_divider():
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Plain)
        divider.setStyleSheet("""
            color: #deded5;
            background-color: #deded5;
            max-height: 1px;
            border: none;
        """)
        return divider

    def toggle_advanced(self, checked):
        self.advanced_container.setVisible(checked)

        self.advanced_btn.setArrowType(
            Qt.ArrowType.DownArrow
            if checked
            else Qt.ArrowType.RightArrow
        )

        self.container.layout().activate()
        self.container.adjustSize()
        self.scroll_area.widget().updateGeometry()

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
            button_text = text_field.text().strip()
            button_url = url_field.text().strip()

            if button_text and button_url:
                buttons.append({
                    "label": button_text,
                    "url": button_url,
                })

        activity_types = {
            "Playing": ActivityType.PLAYING,
            "Listening": ActivityType.LISTENING,
            "Watching": ActivityType.WATCHING,
            "Competing": ActivityType.COMPETING,
        }

        status_display_types = {
            "Name": StatusDisplayType.NAME,
            "State": StatusDisplayType.STATE,
            "Details": StatusDisplayType.DETAILS,
        }

        rpc_data = {
            "activity_type": activity_types[self.activity_type.currentText()],
            "status_display_type": status_display_types[self.status_display_type.currentText()],
            "name": self.name.text().strip() or None,
            "state": self.state.text().strip() or None,
            "details": self.details.text().strip() or None,
            "large_image": self.large_image.text().strip() or None,
            "large_text": self.large_text.text().strip() or None,
            "small_image": self.small_image.text().strip() or None,
            "small_text": self.small_text.text().strip() or None,
            "buttons": buttons or None,
            "start": (int(self.start.text()) if self.start.text() else None),
            "end": (int(self.end.text()) if self.end.text() else None),
            "state_url": self.state_url.text().strip() or None,
            "details_url": self.details_url.text().strip() or None,
            "large_url": self.large_url.text().strip() or None,
            "small_url": self.small_url.text().strip() or None,
            "instance": self.instance.isChecked(),
        }

        try:
            validated_data = RPCDataModel.model_validate(rpc_data)

            data = load_data()
            data["recent"] = rpc_data
            save_data(data)

        except Exception as e:
            self.error_text.setText(str(e))
            return

        self.error_text.clear()

        self.thread = PresenceThread(validated_data)

        self.thread.connected.connect(self.on_rpc_connected)
        self.thread.finished.connect(self.on_thread_finished)
        self.thread.error.connect(self.on_thread_error)

        self.run_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.status.setPixmap(self.loading)

        self.thread.start()

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
