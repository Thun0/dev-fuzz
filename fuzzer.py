import threading
import socket
from sender.message import Message, MessageType
from mutator.mutator import Mutator
import time
import random
import struct


class Fuzzer:

    def __init__(self, dev, port, path, corpus, methods, mutations):
        self.device = dev.device
        self.port = port
        self.running = False
        self.devpath = path
        self.corpus = corpus
        self.methods = methods
        self.mutations = mutations
        print('Fuzzuje {} metody'.format(len(methods)))

    def run(self):
        self.device.forward('tcp:' + str(self.port), 'tcp:' + str(self.port))
        print('Started thread for port {}'.format(self.port))
        self.running = True
        t = threading.Thread(target=self.device.shell, args=('/data/local/tmp/agent {} > /data/local/tmp/out{}'.format(self.port, self.port),))
        #t.start()
        #time.sleep(2) #Wait for agent to create socket
        #TODO: change sleep to receiving ping from agent that it's ready
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect_ex(("localhost", self.port))
        msg = Message(MessageType.DEV_PATH, self.devpath)
        data = msg.pack()
        s.send(data)
        while self.running:
            method = self.methods[random.randrange(0, len(self.methods))]
            corpus_input = self.corpus.get_random_input(method)
            if method is 'ioctl':
                ioctl_req = struct.unpack('q', corpus_input[:8])[0]
                mutator = Mutator(corpus_input[8:])
                mutator.flip_n_bits(random.randint(1, 8*4))
                msg = Message(MessageType.IOCTL, int(ioctl_req), mutator.data)
                data = msg.pack()
                s.send(data)
            elif method is 'write':
                pass
            elif method is 'mmap':
                pass
        s.close()
        print('socket closed - {}', self.port)
        print(t.is_alive())
        t.join()
        print('finished {}'.format(self.port))

    def stop(self):
        self.running = False
