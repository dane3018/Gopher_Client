
from socket import *
from util_functions import send_request, read_response, get_resources
from gopher_crawler import GopherCrawler




def main():
    # Define the server address and port

    # set a timeout of 5 seconds on socket operations 
    host_name = "comp3310.ddns.net"
    portno = 70
    
    crawler = GopherCrawler(hostname=host_name, portno=portno)

    try:
        # Connect to the server
        
        # Send a request
        selector = ""  # Example selector
        sock = send_request(selector, host_name, portno)
        
        # Receive and print the response
        response = read_response(sock, False)

        # resources will be a list of dictionaries
        resources = get_resources(response)
        print(resources)

        # sock = send_request( "/rfc1436.txt")
        # response = read_response(sock, False)
        # print(response)
        
        for res in resources:
            crawler.crawl_resource(res)
        crawler.print_stats()


    # except Exception as e:
    #     print("Error:", e)
    finally:
        # Close the socket
        sock.close()

if __name__ == "__main__":
    main()
