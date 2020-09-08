#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from urllib.parse import urlparse, parse_qs
#from NOM_GPIO import * #import function from another file, this is the way to serve GPIO!
import lib_NOM as LIB
import time

parse_dict = {"abc":"111", "God":"is"}

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s", str(self.path), str(self.headers))
        self._set_response()
        sciezka = str(self.path)
        parseGET = GETparser(sciezka)
        temp = LIB.analogTemperature(0)
        #outputCheckStatus(14)
        self.wfile.write("GOD IS GOOD!\nGET request for {}\nTemperature is: %.2f".format(parseGET).encode('utf-8') % temp)
        time.sleep(2)
        self.wfile.write("Second Message".encode("utf-8"))

    def do_HEADER(self):
        logging.info("HEADER request: %s", str(self.headers))
        self._set_response()
        self.wfile.write("HEADER response")

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def GETparser(path):
    #logging.info("jestem w GETparser")
    parse_dict = parse_qs(urlparse(path).query)
    #checkStatus(2)
    for key in parse_dict:
        print(key,"->",parse_dict[key])
    return parse_dict

def run(server_class=HTTPServer, handler_class=S, port=8081):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
