import threading
import socket
from sender.message import Message, MessageType
from mutator.mutator import Mutator
import time
import random


class Fuzzer:

    def __init__(self, dev, port, path, corpus, methods):
        self.device = dev.device
        self.port = port
        self.running = False
        self.devpath = path
        self.corpus = corpus
        self.methods = methods
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
            corpus_input = self.corpus.get_random_input(random.randrange(0, len(self.methods)))
            print(corpus_input)
            pass #TODO: Fuzzing goes here
            time.sleep(2)
        s.close()
        print('socket closed - {}', self.port)
        print(t.is_alive())
        t.join()
        print('finished {}'.format(self.port))

    def stop(self):
        self.running = False
