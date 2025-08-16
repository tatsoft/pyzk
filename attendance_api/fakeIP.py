import socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 4380))
s.listen(5)
print("Fake device running on 127.0.0.1:4380. Press Ctrl+C to stop.")
while True:
    conn, addr = s.accept()
    print("Connection from", addr)
    conn.close()