import socket
import threading
from tunnel import TUNInterface
from crypto import encrypt, decrypt

# Settings
PORT = 5555
TUN_IP = "10.8.0.1"

# Create TUN interface
tun = TUNInterface(name="tun0", ip=TUN_IP)

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))

print(f"✅ VPN Server running on port {PORT}")

# Store client address
client_addr = None

def from_tun():
    """Read from TUN → encrypt → send to client"""
    while True:
        try:
            packet = tun.read()
            if client_addr:
                encrypted = encrypt(packet)
                sock.sendto(encrypted, client_addr)
        except Exception as e:
            print(f"TUN read error: {e}")

def from_socket():
    """Read from socket → decrypt → write to TUN"""
    global client_addr
    while True:
        try:
            data, addr = sock.recvfrom(65535)
            client_addr = addr
            print(f"📦 Packet from {addr}")
            packet = decrypt(data)
            tun.write(packet)
        except Exception as e:
            print(f"Socket error: {e}")

# Run both in parallel
t1 = threading.Thread(target=from_tun, daemon=True)
t2 = threading.Thread(target=from_socket, daemon=True)

t1.start()
t2.start()

print("✅ VPN is running!")
print("Waiting for client...")

# Keep running forever
t1.join()