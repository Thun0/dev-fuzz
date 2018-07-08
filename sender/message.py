from enum import Enum
import struct


class MessageType(Enum):
    DEV_PATH = 1
    IOCTL = 2
    WRITE = 3
    MMAP = 4


class Message:

    def __init__(self, msg_type, *args):
        self.type = msg_type
        if msg_type == MessageType.DEV_PATH:
            self.path = args[0]
        elif msg_type == MessageType.IOCTL:
            self.req = args[0]
            self.args = args[1]
        else:
            raise NotImplementedError('This type is not supported')

    def pack(self):
        if self.type == MessageType.DEV_PATH:
            return struct.pack('ii{}s'.format(len(self.path)), MessageType.DEV_PATH.value, len(self.path), self.path.encode())
        elif self.type == MessageType.IOCTL:
            raise NotImplementedError('This type is not supported')
        else:
            raise NotImplementedError('This type is not supported')
