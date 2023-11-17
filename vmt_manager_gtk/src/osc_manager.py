from pythonosc import udp_client
from itertools import chain

class OscManager:
    def __init__(self) -> None:
        self.osc = udp_client.SimpleUDPClient("127.0.0.1", 9000)

    def reload_settings(self):
        self.osc.send_message("/VMT/LoadSetting", "")

    def reset_settings(self):
        self.osc.send_message("/VMT/Reset", "")

    def set_room_matrix(self, m):
        self.osc.send_message("/VMT/Set/RoomMatrix", list(chain.from_iterable(m)))
