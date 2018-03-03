import socket
import struct

class Manager:

    connections = []

    def __init__(self):
        pass

    def connect_to_machine(self, addr, port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((addr, port))
            self.connections.append(s)

    def send_data_to(self, data, id):
        header = struct.pack('i', len(data))
        self.connections[id].send(header)
        self.connections[id].send(data)

    def dispose(self):
        for s in self.connections:
            s.close()