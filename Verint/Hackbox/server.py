import socket
import sys
from netfuncs import format_host,recv_header

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allow reuse of address if ungraceful exit
try:
    s.bind(('0.0.0.0', int(sys.argv[1])))
    s.listen(5)
    print('Waiting for connection...')
except:
    s.close()

try:
    while True:
        c_sock, c_addr = s.accept()
        client = format_host(c_addr)
        print('Client ' + client + ' connected.')
        recv_header(c_sock)
        c_sock.close()
        print('Client ' + client + ' disconnected.')
except KeyboardInterrupt:
    s.close()
    print('\nStopping server...')