from pathlib import Path
import json

def client_id_exists():
    path = Path("data/client_id.json")

    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.write_text(json.dumps({}), encoding="utf-8")