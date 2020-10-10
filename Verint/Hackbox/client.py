import socket
import sys
from netfuncs import format_host,send_header

def connect(host,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s_addr = (host,port)
    server = format_host(s_addr)
    print('Connecting to ' + server + '...')
    s.connect(s_addr)
    print('Connected.')
    return s

host,port,*args = sys.argv[1:]
try:
    s = connect(host,int(port))
    send_header(s,*args)
    s.close()
    print('Disconnected.')
except:
    print("Error connecting to server. Make sure the server is running.")