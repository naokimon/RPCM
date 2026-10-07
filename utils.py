from pathlib import Path
import json
import sys

def client_id_exists():
    path = Path("data/client_id.json")

    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.write_text(json.dumps({}), encoding="utf-8")


def resource_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)

        if meipass is None:
            raise RuntimeError("PyInstaller _MEIPASS is unavailable")

        base_path = Path(meipass)
    else:
        base_path = Path(__file__).resolve().parent

    return base_path / relative_path