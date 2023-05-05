import socket
import Protocol


class Player:

    def __init__(self, c_socket, name=None):
        self.c_socket = c_socket
        self.name = name

    def set_name(self, name):
        self.name = name

    def get_msg(self):
        valid, data = Protocol.get_msg(self.c_socket)
        if valid:
            return data
        return ""

    def send_msg(self, msg):
        self.c_socket.send(Protocol.create_msg(msg))
