import os.path
import time

def read_line(socket, chunk=512):
    """
    Read in raw data through socket and convert to line

    Main use will be to retrieve commands and success codes
    """
    buffer = socket.recv(chunk)      # receive 512B data (enough to easily receive commands and reponses)
    data = buffer.decode()
    return data.strip()

def read_data(socket):
    """
    Read in longer data using chunks of 1kB

    return the decoded and stripped text
    """
    buffer = bytearray(1)
    data = b''
    while len(buffer) > 0 and not '\n' in buffer.decode():  # \n indicates end of data
        buffer = socket.recv(1024)
        data+=buffer
    return data.decode().strip()

def send_data(s, data):
    """
    Encode strings into raw data and send
    """
    s.sendall(str.encode(data))

def format_host(addr):
    """
    Format host as  [IP:PORT]
    For example:    [127.0.0.1:8000]
    """
    return f'[{addr[0]}:{addr[1]}]' or addr

def responses(code: str):
    """
    3 digit response codes, similar to FTP, HTTP etc
    1st digit is used for response type: FAIL, SUCCESS, ERROR
    next 2 digits used to identify specific error message

    returns the response type and the message
    """
    r_types = {
        '1':'FAIL',
        '2':'SUCCESS',
        '3':'ERROR'
    }
    responses = {
        '100':'Cannot overwrite existing file',
        '101':'File does not exist',
        '102':'File size does not match',
        '200':'Directory sent',
        '201':'File exists',
        '202':'File received',
        '203':'File sent',
        '204':'File does not already exist',
        '300':'Could not connect',
        '301':'Data not received',
        '302':'Data not sent',
        '303':'Connection closed',
        '399':'Unexpected error'
    }
    return r_types.get(code[0]),responses.get(code)

def log(code,msg=None):
    """
    Log FAIL, SUCCESS and ERROR messages from error codes

    Output: [CODE TYPE]: MSG
    """
    r_type,default_message = responses(str(code))
    print(f'[{code} {r_type}]: {msg or default_message}') # allows for overwriting default message

def send_file(socket, filename):
    """
    Read local file and send raw filedata over the network
    """
    with open(filename,'rb') as f:
        filedata=f.read()
    socket.sendall(filedata)

def recv_file(socket, filename, size=None):
    """
    Receive the raw bytes of a file and 
    write them into a new file
    """
    buffer = bytearray(1)
    data = bytearray()
    bytes_read=0
    if size:
        while bytes_read < size:
            buffer = socket.recv(1024)
            data+=buffer
            bytes_read+=len(buffer)
    else:
        while len(buffer) > 0:
            buffer = socket.recv(1024)
            data+=buffer
            bytes_read+=len(buffer)
    with open(filename,'wb') as f:
        f.write(data)

def send_listing(socket):
    """
    Wrapper for send_data which formats
    and sends the directory list
    """
    send_data(socket,'/'.join(os.listdir()))

def recv_listing(socket):
    """
    Wrapper for read_data to receive
    the formatted directory list and
    print it in a readable form
    """
    data = read_data(socket)
    print('\n'.join(data.split('/')))

def read_response(socket):
    """
    Wrapper to read response codes
    Response codes are 3 bytes

    returns code, (type,message)
    For example:
        '200',('SUCCESS','Directory sent')
    """
    response = read_line(socket,chunk=3)
    return response,responses(response)

def send_header(socket,*args):
    """
    Handles the sending of the header (client)
    From there, it checks command types, responses from the server
    and handles errors in the process.
    """
    args=list(args)
    if len(args) == 1 and args[0].lower() == 'list':
        data='/'.join(args)
        try:
            send_data(socket,data)      # send header
        except:
            log(302)                    # data not sent correctly
            return
        try:
            recv_listing(socket)
        except:
            log(301)                    # data not received correctly
            return
    elif len(args) == 2:
        if args[0].lower() == 'get':
            filename = args[1]
            if os.path.exists(filename):
                log(100)
                return
            data='/'.join(args)
            try:
                send_data(socket,data)
            except:
                log(302)
                return
            try:
                response = read_response(socket)
                if response[0] != '201':
                    log(int(response[0]))
                    return
                filesize = read_line(socket,chunk=20)   # size stored in 20 bytes with padded zeros, allows for large file sizes
                if int(filesize) > 0:
                    recv_file(socket,filename)
                else:
                    open(filename,'a').close()
                if int(filesize) == os.path.getsize(filename):
                    log(202)
                else:
                    log(102)
            except:
                log(301)       # data not received correctly
                return
        elif args[0].lower() == 'put':
            filename = args[1]
            if not os.path.exists(filename):
                log(101)
                return
            args.append(str(os.path.getsize(filename)))  # add filesize to the header
            data='/'.join(args)
            try:
                send_data(socket,data)
            except:
                log(302)
                return
            try:
                response = read_response(socket)
                if response[0] != '204':
                    log(100)
                    return
            except:
                log(301)
                return
            try:
                send_file(socket,filename)                  
            except:
                log(302)
                return
            try:
                response2 = read_response(socket)           # check if success or fail and log
                log(int(response2[0]))
            except:
                log(301)
                return

def recv_header(socket):
    """
    Handles receiving the header (server)
    From here it determines the command and the corresponding
    arguments sent through the header and responds with the 
    appropriate code so that the client knows what to send next
    """
    s = read_line(socket).strip()
    if s == '':
        log(301) # not received correctly
        return
    args = s.split('/')
    if len(args) == 1 and args[0].lower() == 'list':    # LIST
        try:
            send_listing(socket)
            log(200)
        except:
            log(302)
    elif len(args) == 2 and args[0].lower() == 'get':   # GET
        filename = args[1]
        if not os.path.exists(filename):
            try:
                send_data(socket,'101')                     # file not found, do not proceed
                log(101)
                return
            except:
                log(302)
        send_data(socket,'201')                         # file found, send data
        send_data(socket,f'{os.path.getsize(filename):020d}')   # pad with zeros to reach 20 bytes
        try:
            send_file(socket, filename)
            log(203)
        except BrokenPipeError:
            log(303)
    elif len(args) == 3 and args[0].lower() == 'put':   # PUT
        filename,filesize = args[1:]
        if os.path.exists(filename):
            send_data(socket,'100')
            log(100)
            return
        send_data(socket,'204')                         # confirm to client that the file does not already exist
        if int(filesize) > 0:                              
            recv_file(socket,filename,size=int(filesize))
        else:
            open(filename,'a').close()
        if os.path.getsize(filename) == int(filesize):  # check if any corruption/packet loss occurred during transfer
            log(202)
            send_data(socket,'203')
        else:
            log(102)
            send_data(socket,'102')