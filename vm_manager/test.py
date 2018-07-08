import socket
from sender.message import Message, MessageType
import time


def test1():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 42501))
    msg = Message(MessageType.DEV_PATH, '/dev/null')
    data = msg.pack()
    print(data)
    s.send(data)
    time.sleep(1)
    s.close()


test1()
