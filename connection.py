#  pylint: disable=missing-docstring,bad-whitespace
from usb import legacy as usb

class MissileLauncherConnection(object):
    VENDOR_ID = 0x1130
    PRODUCT_ID = 0x0202

    INITA     = (85, 83, 66, 67,  0,  0,  4,  0)
    INITB     = (85, 83, 66, 67,  0, 64,  2,  0)
    CMDFILL   = ( 8,  8,
                  0,  0,  0,  0,  0,  0,  0,  0,
                  0,  0,  0,  0,  0,  0,  0,  0,
                  0,  0,  0,  0,  0,  0,  0,  0,
                  0,  0,  0,  0,  0,  0,  0,  0,
                  0,  0,  0,  0,  0,  0,  0,  0,
                  0,  0,  0,  0,  0,  0,  0,  0,
                  0,  0,  0,  0,  0,  0,  0,  0)
    STOP      = ( 0,  0,  0,  0)
    LEFT      = ( 1,  0,  0,  0)
    RIGHT     = ( 0,  1,  0,  0)
    UP        = ( 0,  0,  1,  0)
    DOWN      = ( 0,  0,  0,  1)
    LEFTUP    = ( 1,  0,  1,  0)
    RIGHTUP   = ( 0,  1,  1,  0)
    LEFTDOWN  = ( 1,  0,  0,  1)
    RIGHTDOWN = ( 0,  1,  0,  1)
    FIRE      = ( 0,  0,  0,  0,  1)

    def __init__(self, index=0):
        self._handle = None
        all_devices = sum((list(bus.devices) for bus in usb.busses()), [])
        launcher_devices = [dev for dev in all_devices
                            if dev.idVendor == self.VENDOR_ID
                            and dev.idProduct == self.PRODUCT_ID]

        self._dev = launcher_devices[index]
        self._conf = self._dev.configurations[0]
        self._intf0 = self._conf.interfaces[0][0]
        #self._intf1 = self._conf.interfaces[1][0]
        self._endpoints0 = list(self._intf0.endpoints)
        #self._endpoints1 = list(self._intf1.endpoints)

        self._handle = self._dev.open()
        self._handle.detachKernelDriver(0)
        self._handle.detachKernelDriver(1)
        #self._handle.setConfiguration(self._conf)
        self._handle.claimInterface(self._intf0)
        #self._handle.setAltInterface(self._intf0)
        self._handle.reset()

    def move(self, x, y):
        assert x in (0, 1, -1)
        assert y in (0, 1, -1)
        left = 1 if x == -1 else 0
        right = 1 if x == 1 else 0
        up = 1 if y == 1 else 0
        down = 1 if y == -1 else 0
        self._move((left, right, up, down))

    def fire(self):
        self._command(self.FIRE)

    def _move(self, direction):
        self._command(direction + (0,))

    def _command(self, command):
        self._handle.controlMsg(0x21, 0x09, self.INITA, 0x02, 0x01)
        self._handle.controlMsg(0x21, 0x09, self.INITB, 0x02, 0x01)
        self._handle.controlMsg(0x21, 0x09, (0,) + command + self.CMDFILL,
                                0x02, 0x01)

class FakeMissileLauncherConnection(object):
    def move(self, x, y):
        print("MOVE {} {}".format(x, y))

    def fire(self):
        print("FIRE")
