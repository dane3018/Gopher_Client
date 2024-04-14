"""
Class to store all fields associated with the assignment specs
and methods to update these values
"""
from util_functions import *
class GopherCrawler:
    def __init__(self):
        self.num_directories = 0
        self.text_files = []
        self.binary_files = []
        self.smallest_text_file_contents = None
        self.largest_text_file_size = 0
        self.smallest_binary_file_size = float('inf')
        self.largest_binary_file_size = 0
        self.num_invalid_references = 0
        self.external_servers = {}  # {server_address: up_status}
        self.error_references = []
    
   
        

    # don't wanna follow a direcotry unless it is a new request 
    def crawl_resource(self, sock, res):
        # Recursive Base cases

        # txt file 
        res_type = res['type']
        selector = res['selector']
        send_request(sock, selector)
        response = read_response(sock)
        if res_type == '0':
            self.handle_txt_file(response)
            self.text_files.append(selector)
            if len(response) < len(self.smallest_text_file_contents):
                response = self.smallest_text_file_contents
            if len(response) > self.largest_text_file_size:
                self.largest_text_file_size = len(response)

    

            





    
