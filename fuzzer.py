class Fuzzer:

    def __init__(self, dev, port):
        self.device = dev
        self.port = port
        dev.forward('tcp:'+str(port), 'tcp:'+str(port))
