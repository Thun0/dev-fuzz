class Fuzzer:

    def __init__(self, dev, port):
        self.device = dev
        self.port = port
        self.running = False
        dev.forward('tcp:'+str(port), 'tcp:'+str(port))

    def run(self):
        print('Started thread for port {}'.format(self.port))
        self.running = True
        while self.running:
            pass

    def stop(self):
        self.running = False
