from util_functions import send_request, read_response, get_resources, check_external_server, write_file
import os


class GopherCrawler:
    """
    Class designed to store important stats relating to the gopher server
    """
    def __init__(self, hostname, portno):
        self.hostname = hostname
        self.portno = portno
        self.num_directories = 0
        self.text_files = []
        self.binary_files = []
        self.smallest_text_file_contents = None
        self.largest_text_file_size = None
        self.smallest_binary_file_size = None
        self.largest_binary_file_size = None
        self.invalid_references = []
        self.external_servers = {}  # {(host, port) : up_status}
        self.error_references = [] # store any references that do not give response
        self.visited_dirs = [] # keep track of which directories have been visited 

    # Other methods and attributes...

    def print_stats(self):
        """
        Note Generated partly by ChatGPT. Used to print all items of the class to stdout 
        """
        print("\nNumber of directories found:", len(self.visited_dirs))
        print(self.visited_dirs)

        print("\nText files found:", len(self.text_files))
        print("\n".join(self.text_files))
        
        print("\nBinary files found:", len(self.binary_files))
        print("\n".join(self.binary_files))
        
        print("\nSmallest text file contents:")
        print(self.smallest_text_file_contents)
        
        print("\nLargest text file size:")
        print(self.largest_text_file_size, "Characters")
        
        print("\nSmallest binary file size:")
        print(self.smallest_binary_file_size, "Bytes")
        
        print("\nLargest binary file size:")
        print(self.largest_binary_file_size, "Bytes")
        
        print("\nNumber of invalid references:")
        print(self.invalid_references)
        
        print("\nExternal servers:")
        for server, status in self.external_servers.items():
            print(f"{server}: {'up' if status else 'down'}")
        
        print("\nError references:")
        print("\n".join(self.error_references))


    def crawl_resource(self, res):
        """
        Recursive function that will crawl every resource 
        on the server and update class fields accordingly. 
        Param res: the resource map to crawl 
        """
        # extract map values
        res_type = res['type']
        selector = res['selector']
        host = res['host']
        port = res['port']
        # already have recorded invalid references before recursive call
        if res_type == '3':
            return
        
        # first check if the resource is an external server
        # update the dict and do not crawl this resource 
        if ((host != 'comp3310.ddns.net' or port != '70') and host != 'invalid'):
                if (host, port) not in self.external_servers:
                    self.external_servers[(host, port)] = check_external_server(host, int(port))
                return
        # Return if we have already seen this directory or initial request
        if (res_type == '1') and (selector in self.visited_dirs) or selector == '':
            return
        
        # get the resource 
        sock = send_request(selector, self.hostname, self.portno)
        is_bin = res_type == '9'
        response = read_response(sock, is_bin)
        if response == None:
            self.error_references.append(selector)
            return

        
        # txt file 
        if res_type == '0':
            self.text_files.append(selector)
            # Maximum file name for downloading a file is 30 chars 
            trim_selector = selector[:30] if len(selector) > 30 else selector
            # create download path
            basename = os.path.basename(trim_selector)
            if not basename.endswith('.txt'):
                basename += '.txt'
            path = os.path.join('output', 'text', basename)
            # download the file 
            write_file(path, response, False)
            # Update smallest text file 
            if not self.smallest_text_file_contents or len(response) < len(self.smallest_text_file_contents):
                self.smallest_text_file_contents = response
            # Update largest text file 
            if not self.largest_text_file_size or len(response) > self.largest_text_file_size:
                self.largest_text_file_size = len(response)


        # directory case add
        elif res_type == '1':
            self.visited_dirs.append(selector)
            response_resources = get_resources(response)
            if not response_resources or response_resources == []:
                return
            # recursively crawl every resource in directory
            for resource in response_resources:
                # if there is an error in the resource, the current selector 
                # is invalid
                if resource['type'] == '3':
                    self.invalid_references.append(selector)
                self.crawl_resource(resource)
            
        # binary file case
        elif res_type == '9':
            self.binary_files.append(selector)
            basename = os.path.basename(selector)
            path = os.path.join('output', 'bin', basename)
            # download file 
            write_file(path, response, True)
            if self.largest_binary_file_size == None:
                self.largest_binary_file_size = len(response)
            if self.smallest_binary_file_size == None:
                self.smallest_binary_file_size = len(response)
            self.largest_binary_file_size = max(self.largest_binary_file_size, len(response))
            self.smallest_binary_file_size = min(self.smallest_binary_file_size, len(response))
        
            
        else: print("different type of resource")

    
    
            



