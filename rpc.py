import time
from pypresence import Presence

def set_presence(data):
    presence: Presence = Presence(data["client_id"], pipe=0)

    presence.connect()

    presence.update()

    while True:
        time.sleep(5)
