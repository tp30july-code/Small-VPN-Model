import socket
import threading
from tunnel import TUNInterface
from crypto import encrypt, decrypt

# Settings
SERVER_IP = "127.0.0.1"   # change to server IP later
SERVER_PORT = 5555
TUN_IP = "10.8.0.2"       # different IP from server!

# Create TUN interface
tun = TUNInterface(name="tun1", ip=TUN_IP)

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server = (SERVER_IP, SERVER_PORT)

print(f"✅ VPN Client connecting to {SERVER_IP}:{SERVER_PORT}")

def from_tun():
    """Read from TUN → encrypt → send to server"""
    while True:
        try:
            packet = tun.read()
            encrypted = encrypt(packet)
            sock.sendto(encrypted, server)
            print(f"📤 Sent encrypted packet")
        except Exception as e:
            print(f"TUN read error: {e}")

def from_socket():
    """Read from socket → decrypt → write to TUN"""
    while True:
        try:
            data, _ = sock.recvfrom(65535)
            packet = decrypt(data)
            tun.write(packet)
            print(f"📥 Received encrypted packet")
        except Exception as e:
            print(f"Socket error: {e}")

# Run both in parallel
t1 = threading.Thread(target=from_tun, daemon=True)
t2 = threading.Thread(target=from_socket, daemon=True)

t1.start()
t2.start()

print("✅ VPN Client is running!")

# Keep running forever
t1.join()