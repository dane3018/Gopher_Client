# Gopher_Client

## Files
gopher_client.py: main function, run this file to run the client
gopher_crawler.py: file with the GopherCrawler class which is used to store fields that will be printed after crawling
util_functions.py: utility functions that do not need to be encapsulated by the GopherCrawler class 

## Clarifications 
A timeout value of 5 seconds is set for all socket operations. This also means that if the server is continuously sending data for longer than 5 seconds, the client will stop receiving data and disregard the previously sent data. While 5 seconds is somewhat arbitrary, this was decided so that the crawling did not take too long and most servers should respons within 5 seconds. This value can be changed easily in the global variable timeout_value in util_functions