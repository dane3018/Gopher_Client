"""
Class to store all fields associated with the assignment specs
and methods to update these values
"""
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
    
