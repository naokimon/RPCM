# RPCM — Rich Presence Manager

A small Windows desktop app for setting a **custom Discord Rich Presence** without writing any code.

You enter a Discord application's Client ID, fill in a few fields (name, state, details, images, timestamps), press **Run**, and that activity shows on your Discord profile until you press **Stop**.

Built with Python, PySide6 (GUI), and pypresence (Discord IPC).

## Requirements

- Windows (the config path is hardcoded to `%APPDATA%`)
- Discord **desktop app**, running and logged in (pypresence talks to it over local IPC)
- Python 3.10+ if running from source
- A Discord application created in the [Developer Portal](https://discord.com/developers/home) (this is where you get the Client ID and upload image assets)

## Run from source

```bash
git clone https://github.com/naokimon/RPCM.git
cd RPCM
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Usage

1. Click **Set Client ID**, paste your application's Client ID, and click **Validate**. A green check means Discord recognized it, and it is saved.
2. Fill in whichever fields you want (all optional, see below).
3. Click **Run**. The status icon shows loading, then a green check once connected.
4. Click **Stop** to clear the presence and disconnect.

Your Client ID and the last fields you ran with are saved and restored on the next launch.

### Fields

| Field | What it does |
|---|---|
| Name | Activity name |
| State | Second line of text (e.g. "In a group") |
| Details | First line of text (e.g. "Playing solo") |
| Large image | Asset key of the large image (uploaded under your app's Rich Presence art assets) |
| Large text | Tooltip shown when hovering the large image |
| Small image | Asset key of the small corner image |
| Small text | Tooltip shown when hovering the small image |
| Start | Unix timestamp in seconds. Discord shows time elapsed since then |
| End | Unix timestamp in seconds. Discord shows time remaining until then |

Empty fields are not sent. The presence is re-sent every 5 seconds while running.

## Data storage

Saved to `%APPDATA%\RPCM\config.json`:

```json
{
    "client_id": "123456789012345678",
    "recent": { "name": "...", "state": "...", "details": "...", "...": "..." }
}
```

Delete this file to reset the app.

## Build a standalone .exe

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --name main --icon src/images/RPCM.ico --add-data "src/images;src/images" main.py
```

Output: `dist/main.exe`. The `--add-data` flag bundles the icons and status images; the app finds them at runtime through `resource_path()` in `utils.py`.

## Project structure

| File | Purpose |
|---|---|
| `main.py` | Entry point. Creates the app, enforces a single running instance, opens the 1080x720 main window |
| `gui.py` | UI. `MainWindow` (the presence form, Run/Stop, status icon) and `ClientIdWindow` (Client ID entry and validation against Discord's API) |
| `rpc.py` | `PresenceThread`: a background `QThread` that connects to Discord, sends the presence every 5 seconds, and clears it on stop |
| `schemas.py` | `RPCDataModel`: Pydantic model describing the presence payload |
| `utils.py` | Load/save `config.json` and resolve resource paths (works both from source and from the PyInstaller exe) |
| `requirements.txt` | Dependencies: `requests`, `pyside6`, `pypresence`, `pydantic` |
| `main.spec` | PyInstaller build spec (bundles `src/images`, windowed, uses `RPCM.ico`) |
| `src/images/` | `RPCM.ico` / `RPCM.png` (app icon), `check.png` / `close.png` / `loading.png` (status icons) |
| `.gitignore` | Ignores `.idea/`, `.venv/`, `__pycache__/`, `data/`, `dist/`, `build/` |


## Limitations

- Windows only.
- The UI exposes 9 fields. `schemas.py` also defines buttons, party size, activity type, URLs, and match/join/spectate fields, but there is no UI for them yet.
- Only one presence can run at a time, and only one app window can be open.
