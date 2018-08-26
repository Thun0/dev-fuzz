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
        if self.rooted:
            self.name += '(root)'

    def install(self, path):
        dest = '/data/local/tmp/{}'.format(path.split('/')[-1])
        self.device.push(path, dest, mode=0o755)
        self.device.shell('pm install {}'.format(dest))

    def install_busybox(self):
        self.install("busybox.apk")
        self.device.shell("echo 'mount -o rw,remount -t ext4 /system' | su")
        self.device.shell("echo 'cp /data/data/stericson.busybox/files/bb/busybox /system/xbin' | su")
        self.device.shell("echo 'chmod 755 /system/xbin/busybox' | su")

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

    def get_char_devices(self):
        if not self.rooted:
            return []
        ret = []
        output = self.device.shell("su -c 'busybox find /dev/ -type c | busybox sort'").split('\n')
        for d in output:
            if d.strip() is not '':
                attrs = self.device.shell("su -c 'ls -l {}'".format(d.strip())).strip().split()
                if attrs[0][0] is 'c':
                    ret.append('{} {} {} {}'.format(attrs[0], attrs[1], attrs[2], d.strip()))
        return ret
