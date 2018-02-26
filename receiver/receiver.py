import socket
import settings
import threading

class Receiver:

    connections = []

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((socket.gethostname(), settings.config["receiver"]["port"]))
        self.sock.listen(5)
        self.thr = threading.Thread(target=self.thread_function())
        self.thr.start()

    def thread_function(self):
        while True:
            conn, addr = self.sock.accept()
            self.connections.append(conn)
            print("Connection from " + addr)
            # FIXME: rest of the function
