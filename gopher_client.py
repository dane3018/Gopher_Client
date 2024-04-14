import socket
from socket import *
from util_functions import *

def main():
    # Define the server address and port
    server_address = "comp3310.ddns.net"
    server_port = 70

    # Create a TCP socket
    sock = socket(AF_INET, SOCK_STREAM)
    
    try:
        # Connect to the server
        sock.connect((server_address, server_port))
        
        # Send a request
        selector = ""  # Example selector
        send_request(sock, selector)
        
        # Receive and print the response
        response = read_response(sock)
        print("Response from server:")
        # resources will be a list of dictionaries
        resources = get_resources(response)
        print(resources)


    except Exception as e:
        print("Error:", e)
    finally:
        # Close the socket
        sock.close()

if __name__ == "__main__":
    main()
