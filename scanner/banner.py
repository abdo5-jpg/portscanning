import socket

def grab_banner(target, port, timeout=2):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((target, port))
            s.send(b'HEAD / HTTP/1.0\r\n\r\n')
            banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            return banner[:150] if banner else "No banner"
    except:
        return "No banner / Filtered"