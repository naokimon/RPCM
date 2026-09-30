from PySide6.QtWidgets import QMainWindow, QWidget, QFormLayout, QLineEdit, QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QIcon, QIntValidator, QPixmap
from rpc import set_presence
from schemas import RPCDataModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RPCM")
        self.setWindowIcon(QIcon("src/images/RPCM.png"))

        container = QWidget()
        self.setCentralWidget(container)

        layout = QVBoxLayout(container)
        form = QFormLayout()

        int_validator = QIntValidator()

        self.client_id = QLineEdit()
        self.client_id.setValidator(int_validator)

        self.name = QLineEdit()
        self.state = QLineEdit()
        self.details = QLineEdit()

        form.addRow("Client ID:", self.client_id)
        form.addRow("Name:", self.name)
        form.addRow("State:", self.state)
        form.addRow("Details:", self.details)

        self.large_image = self.add_file_field(
            form, "Large image:"
        )
        self.large_text = QLineEdit()
        form.addRow("Large text:", self.large_text)

        self.small_image = self.add_file_field(
            form, "Small image:"
        )
        self.small_text = QLineEdit()
        form.addRow("Small text:", self.small_text)

        self.start = QLineEdit()
        self.start.setValidator(int_validator)

        self.end = QLineEdit()
        self.end.setValidator(int_validator)

        form.addRow("Start:", self.start)
        form.addRow("End:", self.end)

        submit_row = QHBoxLayout()

        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.submit)

        self.status_img = QPixmap("./src/images/close.png")
        self.status = QLabel()
        self.status.setPixmap(self.status_img)
        self.status.setScaledContents(True)
        self.status.setFixedSize(25, 25)

        submit_row.addWidget(submit_btn)
        submit_row.addWidget(self.status)

        layout.addLayout(form)
        layout.addLayout(submit_row)

    def add_file_field(self, form, label):
        line_edit = QLineEdit()
        browse_btn = QPushButton("Browse...")

        browse_btn.clicked.connect(
            lambda: self.select_image(line_edit)
        )

        widget = QWidget()
        row = QHBoxLayout(widget)
        row.setContentsMargins(0, 0, 0, 0)

        row.addWidget(line_edit)
        row.addWidget(browse_btn)

        form.addRow(label, widget)

        return line_edit

    def select_image(self, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )

        if file_path:
            line_edit.setText(file_path)

    def submit(self):
        data = {

        }

        print(self.name.text())