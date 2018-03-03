import socket
import settings
import struct


class Receiver:
    """Receiver class which runs on guest, receives data and sends it to driver
    """

    sock = None

    def __init__(self, port=settings.config["receiver"]["port"]):
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_sock.bind(("localhost", port))
        self.listen_sock.listen(5)
        self.sock, addr = self.listen_sock.accept()
        print("Connection from " + addr[0])

    def run(self):
        while True:
            pass
            # FIXME: receive data and send to driver

    def receive_data(self):
        length = struct.unpack('i', self.sock.recv(4))[0]
        print(length)
        return self.sock.recv(length)

    def dispose(self):
        self.listen_sock.close()

    def test_receive(self):
        return self.receive_data()