import socket
import utils

def send_udp():
    if not utils.ip_address:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('8.8.8.8', 80))
        utils.ip_address = s.getsockname()[0]
        print(utils.ip_address)
    message = f"ws://{utils.ip_address}:{utils.PORT},{utils.Pc_name}".encode("utf-8")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(message, ("255.255.255.255", 5000))
    sock.close()