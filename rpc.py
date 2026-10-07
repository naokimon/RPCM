import json
from pypresence import Presence
from schemas import RPCDataModel
from PySide6.QtCore import QThread, Signal


class PresenceThread(QThread):
    finished = Signal()
    error = Signal(str)

    def __init__(self, data: RPCDataModel, parent=None):
        super().__init__(parent)

        self.data = data
        self.running = True
        self.presence = None

    def stop(self):
        self.running = False

    def run(self):
        try:
            with open("data/client_id.json", encoding="utf-8") as f:
                client_data = json.load(f)

            client_id = client_data["client_id"]

            self.presence = Presence(client_id)
            self.presence.connect()

            while self.running:
                self.presence.update(
                    **self.data.model_dump(exclude_none=True)
                )

                self.msleep(15_000)

        except Exception as e:
            self.error.emit(str(e))

        finally:
            if self.presence is not None:
                try:
                    self.presence.close()
                except Exception as e:
                    print(e)

                self.presence = None

            self.finished.emit()