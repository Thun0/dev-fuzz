import socket
from sender.message import Message, MessageType
import time
from mutator import mutator

def test1():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 57001))
    s.close()
    msg = Message(MessageType.DEV_PATH, '/dev/null')
    data = msg.pack()
    print(data)
    s.send(data)
    msg = Message(MessageType.IOCTL, 13371337, 'ablablablablabala'.encode())
    data = msg.pack()
    print(data)
    s.send(data)
    time.sleep(1)
    s.close()


def test2():
    m = Mutator()


test2()
