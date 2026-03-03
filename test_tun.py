# test_tun.py
from tunnel import TUNInterface

# Create TUN interface
tun = TUNInterface(
    name="tun0",
    ip="10.8.0.1",
    netmask="255.255.255.0"
)

print("Waiting for packets...")
print("Open new terminal and run: ping 10.8.0.1")
print("You will see packets here!")

# Read packets
while True:
    packet = tun.read()
    print(f"Got packet! Size: {len(packet)} bytes")
    print(f"First 20 bytes: {packet[:20]}")
    print("─────────────────────────")