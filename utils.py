from pathlib import Path
import json
import sys

appdata_dir = Path.home() / "AppData" / "Roaming" / "RPCM"

appdata_dir.mkdir(parents=True, exist_ok=True)

config_file = appdata_dir / "config.json"

def save_data(data):
    with config_file.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_data():
    if not config_file.exists():
        return {}

    try:
        with config_file.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def resource_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)

        if meipass is None:
            raise RuntimeError("PyInstaller _MEIPASS is unavailable")

        base_path = Path(meipass)
    else:
        base_path = Path(__file__).resolve().parent

    return base_path / relative_path

def get_stylesheet(theme):
    stylesheet = f"""
        QMainWindow, QWidget {{
            background: {theme["window_bg"]};
            color: {theme["text"]};
            font-family: "{theme["font_family"]}", sans-serif;
            font-size: {theme["font_size"]};
        }}

        QLabel {{ background: transparent; }}

        QLabel#clientIdValue {{
            color: {theme["muted_text"]};
            background: {theme["surface_alt"]};
            border: 1px solid {theme["border_subtle"]};
            padding: 7px 9px;
            font-weight: 600;
        }}

        QLineEdit, QComboBox {{
            background: {theme["surface"]};
            color: {theme["text"]};
            border: 1px solid {theme["border"]};
            border-radius: {theme["radius"]};
            padding: 7px 9px;
            min-height: 18px;
            selection-background-color: {theme["accent"]};
            selection-color: {theme["white"]};
        }}

        QLineEdit:hover, QComboBox:hover {{
            border-color: {theme["border_hover"]};
        }}

        QLineEdit:focus, QComboBox:focus {{
            border: 1px solid {theme["accent_focus"]};
            background: {theme["surface"]};
        }}

        QLineEdit:disabled, QComboBox:disabled {{
            color: {theme["disabled_text"]};
            background: {theme["disabled_bg"]};
            border-color: {theme["disabled_border"]};
        }}

        QComboBox::drop-down {{
            border: none;
            width: 24px;
        }}

        QComboBox QAbstractItemView {{
            background: {theme["surface"]};
            color: {theme["text"]};
            border: 1px solid {theme["border"]};
            selection-background-color: {theme["selection_bg"]};
            selection-color: {theme["text"]};
            outline: none;
        }}

        QPushButton {{
            background: {theme["surface_alt"]};
            color: {theme["button_text"]};
            border: 1px solid {theme["border"]};
            border-radius: {theme["radius"]};
            padding: 8px 12px;
            font-weight: 500;
        }}

        QPushButton:hover {{
            background: {theme["panel_bg"]};
            border-color: {theme["border_strong"]};
        }}

        QPushButton:pressed {{
            background: {theme["selection_bg"]};
        }}

        QPushButton:disabled {{
            color: {theme["disabled_text"]};
            background: {theme["disabled_bg"]};
            border-color: {theme["disabled_border"]};
        }}

        QPushButton#secondaryButton {{
            background: transparent;
            border-color: {theme["border"]};
            text-align: left;
        }}

        QPushButton#secondaryButton:hover {{
            background: {theme["surface_alt"]};
        }}

        QPushButton#primaryButton {{
            background: {theme["accent"]};
            border: 1px solid {theme["accent"]};
            color: {theme["white"]};
            min-width: 150px;
        }}

        QPushButton#primaryButton:hover {{
            background: {theme["accent_hover"]};
            border-color: {theme["accent_hover"]};
        }}

        QPushButton#primaryButton:pressed {{
            background: {theme["accent_pressed"]};
            border-color: {theme["accent_pressed"]};
        }}

        QPushButton#dangerButton {{
            background: transparent;
            border: 1px solid {theme["border"]};
            color: {theme["danger"]};
            min-width: 150px;
        }}

        QPushButton#dangerButton:hover {{
            background: {theme["danger_bg_hover"]};
            border-color: {theme["danger_border_hover"]};
        }}

        QToolButton {{
            color: {theme["button_text"]};
            font-size: {theme["font_size"]};
            font-weight: 600;
            border: none;
            border-radius: {theme["radius"]};
            padding: 8px 2px;
            text-align: left;
        }}

        QToolButton:hover {{
            color: {theme["accent"]};
        }}

        QFrame#advancedPanel {{
            background: {theme["panel_bg"]};
            border: 1px solid {theme["border_subtle"]};
            border-radius: {theme["radius"]};
        }}

        QCheckBox {{
            spacing: 8px;
        }}

        QCheckBox::indicator {{
            width: 15px;
            height: 15px;
            border-radius: 2px;
            background: {theme["surface"]};
            border: 1px solid {theme["border_strong"]};
        }}

        QCheckBox::indicator:hover {{
            border-color: {theme["accent_focus"]};
        }}

        QCheckBox::indicator:checked {{
            background: {theme["accent"]};
            border-color: {theme["accent"]};
        }}

        QCheckBox:disabled {{
            color: {theme["disabled_text"]};
        }}

        QLabel#errorText {{
            color: {theme["error"]};
            padding: 2px 0;
        }}

        QLabel#connectionStatus {{
            padding: 6px;
        }}
           QScrollBar:vertical {{
            background: {theme["surface_alt"]};
            width: 10px;
            margin: 2px 2px 2px 2px;
            border: none;
            border-radius: 5px;
        }}
        QScrollBar::handle:vertical {{
            background: {theme["border_strong"]};
            min-height: 30px;
            border-radius: 5px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: {theme["accent"]};
        }}

        QScrollBar::handle:vertical:pressed {{
            background: {theme["accent_hover"]};
        }}

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0px;
            border: none;
            background: none;
        }}

        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {{
            background: none;
        }}

        QScrollBar:horizontal {{
            background: {theme["surface_alt"]};
            height: 10px;
            margin: 2px 2px 2px 2px;
            border: none;
            border-radius: 5px;
        }}

        QScrollBar::handle:horizontal {{
            background: {theme["border_strong"]};
            min-width: 30px;
            border-radius: 5px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background: {theme["accent"]};
        }}

        QScrollBar::handle:horizontal:pressed {{
            background: {theme["accent_hover"]};
        }}

        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {{
            width: 0px;
            border: none;
            background: none;
        }}

        QScrollBar::add-page:horizontal,
        QScrollBar::sub-page:horizontal {{
            background: none;
        }}
    """

    return stylesheet