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
from dicttoxml import dicttoxml
import json
import I2C_LCD_driver as LCD

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
        operationMode = str(parseGET.get("operation"))[2:-2]
        print(operationMode)
        
        
        if operationMode == "getAll":
         LCD_operationMode(operationMode)
         allData = json.dumps(LIB.getAllData())
        elif operationMode == "getByName":
         byName = str(parseGET.get("eqName"))[2:-2]
         LCD_operationMode("%s:%s" % (operationMode,byName))
         rep = []
         rep.append(LIB.getByName(byName))
         allData = json.dumps(rep)
        elif operationMode == "setByName":
         byName = str(parseGET.get("eqName"))[2:-2]
         byName_val = str(parseGET.get("eqVal"))[2:-2]
         LCD_operationMode("%s:%s" % (operationMode,byName))
         rep = []
         rep.append(LIB.setByName(byName,byName_val))
         allData = json.dumps(rep)
        elif operationMode =="DecisionSystem":
         LCD_operationMode("%s" % (operationMode))
         db_rules = str(parseGET.get("selection"))[2:-2]
         db_rules
         db_json = db_rules.strip('}][{').split('}, ')
         db_query = []
         for x in db_json:
             db_temp = {}
             for y in x.split(','):
                z = y.split('=')
                db_temp[str.strip(z[0]).replace("{","")] = str.strip(z[1]).replace("{","")
             db_query.append(db_temp)   
         reply = []
         for t in db_query:
             instrument = t["instrument_name"]
             upLimit = t["upper_limit"]
             loLimit = t["lower_limit"]
             regulator = t["regulator_name"]
             upRule = t["upper_rule"]
             loRule = t["lower_rule"]
             reply = reply + (LIB.DecisionSystem(instrument, upLimit, loLimit, regulator, upRule, loRule))
         allData = json.dumps(reply)
        print("SENDED DATA: \n%s" % allData) 
        self.wfile.write("{}".format(allData).encode('utf-8'))

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
    parse_dict = parse_qs(urlparse(path).query)
    #for key in parse_dict:
    #   print(key,"->",parse_dict[key])
    return parse_dict

def run(server_class=HTTPServer, handler_class=S, port=8081):
    intro()
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

def intro():
    LIB.bip(0.1,2,0.1)
    time.sleep(0.5)
    LIB.bip(0.1,2,0.1)
    time.sleep(0.5)
    LIB.bip(0.1,2,0.1)
    return True

def LCD_operationMode(mode):
    mylcd = LCD.lcd()
    stringTime = time.strftime("%H:%M:%S", time.localtime())
    mylcd.lcd_display_string(mode,1)
    mylcd.lcd_display_string(stringTime,2)
    return True

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
