import socket

class Manager:

    vms = []
    connections = []

    def __init__(self):
        pass

    def connect_to_machine(self, addr, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((addr, port))
            self.connections.append(s)
