from datetime import datetime
import socket
from socket import *
import time


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
    sock.settimeout(5)
    start_time = time.time()
    try:
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
            if not is_binary and ch.endswith(b'\r\n.\r\n'):
                break
            # if receiving data for longer than 5 seconds
            if time.time() - start_time > 5:
                print('timeout')
                sock.close()
                return None
        sock.close()
        if is_binary:
            return in_data
        txt = in_data.decode('utf-8', 'backslashreplace')
        return remove_terminator(txt)
    except Exception as e:
        print("timeout:", e)
        sock.close()
        return None
    
def remove_terminator(txt):
    # edge case where .txt file is empty no leading new line
    if txt == ".\r\n":
        return ""
    suffix = "\r\n.\r\n"
    if txt.endswith(suffix):
        return txt[:-len(suffix)]
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
    # error code
    # if txt.startswith('3'):
    #     return [txt.split('\r\n')[0],]
    resources = txt.split('\r\n')
    result = []

    for res in resources:
        if(res.startswith(('0','1','2','3','9'))):
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
        # if(res.startswith('3')):
        #     current = {
                
        #     }

    return result






def check_external_server(host_name, portno):
        server_up = False
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host_name, portno))
            server_up = True
        finally:
            sock.close()
            return server_up


