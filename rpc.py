import json
from threading import Event
from pypresence import Presence
from schemas import RPCDataModel
from PySide6.QtCore import QThread, Signal


class PresenceThread(QThread):
    connected = Signal()
    error = Signal(str)

    def __init__(self, data: RPCDataModel, parent=None):
        super().__init__(parent)

        self.data = data
        self.stop_event = Event()
        self.set = False
        self.presence = None

    def stop(self):
        self.stop_event.set()

    def run(self):
        try:
            with open("data/client_id.json", encoding="utf-8") as f:
                client_data = json.load(f)

            client_id = client_data["client_id"]

            self.presence = Presence(client_id)
            self.presence.connect()

            self.connected.emit()

            payload = self.data.model_dump(exclude_none=True)

            while not self.stop_event.is_set():
                self.presence.update(**payload)

                if self.stop_event.wait(5):
                    break

        except Exception as e:
            self.error.emit(str(e))

        finally:
            if self.presence is not None:
                try:
                    self.presence.clear()
                    self.presence.close()
                except Exception as e:
                    print(e)

                self.presence = None