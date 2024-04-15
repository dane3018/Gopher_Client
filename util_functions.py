from datetime import datetime
import socket
from socket import *


# Sock Line functions 

def send_request(req, host_name, portno):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((host_name, portno))
    txt = req+'\r\n'
    sock.sendall(txt.encode('utf-8'))
    log_request(req)
    return sock

def read_response(sock, is_binary):
    """
    Read single line terminated by \r\n from sock, or None if closed.
    Param is_binary: boolean
        variable to check whether the response will be a binary file
        if so, do not want to check for new line, period, new line pattern
    
    """
    # Read as bytes. Only convert to UTF-8 when we have entire line.
    in_data = b''
    while True:
        ch = sock.recv(4096)
        if len(ch) == 0:
            # Socket closed. If we have any data it is an incomplete
            # line, otherwise immediately return None
            if len(in_data) > 0:
                break
            else:
                return None
        in_data += ch
        # this pattern indicates the end of the request
        if ch.endswith(b'\r\n.\r\n'):
            break
    # if is_binary:
    #     return in_data
    txt = in_data.decode('utf-8', 'backslashreplace')
    sock.close()
    return txt





# used for every request to the server
def log_request(request):
    timestamp = datetime.now()
    print('Sending request:', '"'+request+'"', 'at time:', timestamp)


# general functions 
def get_resources(txt):
    """
    Takes a response string and converts it into a dictionary 
    with its key fields or None if 
    """
    if not txt:
        return None
    resources = txt.split('\r\n')
    result = []

    for res in resources:
        if(res.startswith(tuple(str(i) for i in range(10)))):
            values = res.split('\t')
            
            if len(values) != 4:
                return None # each resource should have 4 tab delimitted values
            current = {
                'type': values[0][0],  # first char
                'name': values[0][1:],  # rest of the first value
                'selector': values[1],
                'host': values[2],
                'port': values[3]
            }
            result.append(current)

    return result



def count_dirs(txt):
    return 0

