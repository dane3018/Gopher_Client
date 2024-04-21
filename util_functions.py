from datetime import datetime
import socket
from socket import *
import time
import os

timeout_value = 5 #change timout of sock operations here


# Sock Line functions 

def send_request(req, host_name, portno):
    """
    Send request 'req' using socket to host_name and portno
    """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.settimeout(timeout_value)
    sock.connect((host_name, portno))
    txt = req+'\r\n'
    sock.sendall(txt.encode('utf-8'))
    log_request(req)
    return sock

def read_response(sock, is_binary):
    """
    Read a response terminated by '\r\n.\r\n' from sock, or until EOF reached 
    for binary files. Return the response as a text or bytes for binary files.
    return None if socket operation fails. 
    """
    # Read as bytes. Only convert to UTF-8 when we have entire line.
    sock.settimeout(timeout_value)
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
            if time.time() - start_time > timeout_value:
                print('Reached timeout value when receiving data')
                sock.close()
                return None
        sock.close()
        if is_binary:
            return in_data
        txt = in_data.decode('utf-8', 'backslashreplace')
        return remove_terminator(txt)
    # socket.timeout occurred
    except timeout:
        print("Socket operation timed out")
        sock.close()
        return None
    except Exception as e:
        print("Error reading data", e)
        sock.close()
        return None
    
def write_file(path, content, is_binary):
    """
    Writes the contents of 'content' to the file at 'path'
    """
    try:
        flag = 'wb+' if is_binary else 'w+'
        with open(path, flag) as file:
            file.write(content)
            file.close()
    except Exception as e:
        print("Unable to write to file:", path, e)

    
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


def get_resources(txt):
    """
    Takes a response string and converts it into a dictionary 
    with its key fields or None if data is malformed 
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

    return result






def check_external_server(host_name, portno):
        """
        Opens a socket with host_name and portno and 
        attempts to connect. If successful will return True
        """
        server_up = False
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host_name, portno))
            server_up = True
        finally:
            sock.close()
            return server_up


