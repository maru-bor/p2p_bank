import socket

def get_own_ip():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
    except Exception:
        ip = "127.0.0.1"
    return ip

