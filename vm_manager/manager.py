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

    def send_data_to(self, data, connid):
        header = struct.pack('i', len(data))
        self.connections[connid].send(header)
        self.connections[connid].send(data)

    def dispose(self):
        for s in self.connections:
            s.close()
