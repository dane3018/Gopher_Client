from datetime import datetime


# Sock Line functions 

def send_request(sock, req):
    txt = req+'\r\n'
    sock.sendall(txt.encode('utf-8'))
    log_request(req)

def read_response(sock):
    """Read single line terminated by \r\n from sock, or None if closed."""
    # Read as bytes. Only convert to UTF-8 when we have entire line.
    inData = b''
    while True:
        ch = sock.recv(4096)
        if len(ch) == 0:
            # Socket closed. If we have any data it is an incomplete
            # line, otherwise immediately return None
            if len(inData) > 0:
                break
            else:
                return None
        inData += ch
        # this pattern indicates the end of the request
        if ch.endswith(b'\r\n.\r\n'):
            break
    txt = inData.decode('utf-8', 'backslashreplace')
    return txt





# used for every request to the server
def log_request(request):
    timestamp = datetime.now()
    print('Sending request:', '"'+request+'"', 'at time:', timestamp)


# general functions 
def get_resources(txt):
    """
    Takes a response string and converts it into a dictionary 
    with its key fields. 
    """
    resources = txt.split('\r\n')
    result = []

    for res in resources:
        if(res.startswith(tuple(str(i) for i in range(10)))):
            values = res.split('\t')
            
            if len(values) != 4:
                raise Exception('Response line has less than 4 tab delimmitted attributes', values)
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

