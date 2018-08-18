class AndroidDevice:

    def __init__(self, dev):
        self.device = dev
        self.serial = dev.serial
        self.manufacturer = dev.get_properties()['ro.product.manufacturer']
        if self.manufacturer == 'unknown':
            self.name = '{}({}): {}'.format(dev.get_properties()['ro.product.model'],
                                            dev.get_properties()['ro.product.device'], self.serial)
        else:
            self.name = '{}-{}({}): {}'.format(self.manufacturer, dev.get_properties()['ro.product.model'],
                                               dev.get_properties()['ro.product.device'], self.serial)
        self.rooted = False
        self.check_root()

    def check_root(self):
        if str(self.device.shell("echo 'id' | su"))[:11] == 'uid=0(root)':
            self.rooted = True
        else:
            try:
                self.device.root()
            except RuntimeError as e:
                if str(e) == 'adbd cannot run as root in production builds':
                    self.rooted = False
                elif str(e) == 'adbd is already running as root':
                    self.rooted = True
                else:
                    raise RuntimeError(str(e))
