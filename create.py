import pytun

class TUNInterface:
    def __init__(self, name="tun0", ip="10.8.0.1", netmask="255.255.255.0", mtu=1500):
        self.tun = pytun.TunTapDevice(
            name=name,
            flags=pytun.IFF_TUN | pytun.IFF_NO_PI
        )
        self.tun.addr    = ip
        self.tun.netmask = netmask
        self.tun.mtu     = mtu
        self.tun.up()
        print(f"✅ TUN interface {name} is UP!")
        print(f"✅ IP Address: {ip}")

    def read(self) -> bytes:
        return self.tun.read(self.tun.mtu)

    def write(self, data: bytes):
        self.tun.write(data)

    def fileno(self):
        return self.tun.fileno()