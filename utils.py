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

    with config_file.open("w", encoding="utf-8") as f:
        return json.load(f)


def resource_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)

        if meipass is None:
            raise RuntimeError("PyInstaller _MEIPASS is unavailable")

        base_path = Path(meipass)
    else:
        base_path = Path(__file__).resolve().parent

    return base_path / relative_path