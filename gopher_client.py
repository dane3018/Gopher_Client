
from socket import *
from util_functions import send_request, read_response, get_resources
from gopher_crawler import GopherCrawler
import os

def main():
    # Define the server address and port

    # set a timeout of 5 seconds on socket operations 
    host_name = "comp3310.ddns.net"
    portno = 70
    
    crawler = GopherCrawler(hostname=host_name, portno=portno)
    # ensure ouput directories exist
    base_dir = 'output'
    os.makedirs(base_dir, exist_ok=True)

    # Create the 'output/text' directory
    text_dir = os.path.join(base_dir, "text")
    os.makedirs(text_dir, exist_ok=True)

    # Create the 'output/bin' directory
    bin_dir = os.path.join(base_dir, "bin")
    os.makedirs(bin_dir, exist_ok=True)
    try:
        # Send initial request
        selector = ""  # Example selector
        sock = send_request(selector, host_name, portno)
        
        response = read_response(sock, False)

        # get each resources as a dictionary
        resources = get_resources(response)

        # Crawl each resource and update object fields
        for res in resources:
            crawler.crawl_resource(res)
        # Print all stats recorded from the server
        crawler.print_stats()

    except Exception as e:
        print('gopher client error:')
        raise e


if __name__ == "__main__":
    main()
