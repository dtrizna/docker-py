from http.server import BaseHTTPRequestHandler,HTTPServer
import requests
import time
import os

HOST_NAME = ''
PORT_NUMBER = 80
COUNTER = 0

# try to take number of HTTP servers to balance
# from env variables to set up during build
try:
    SERVERS = int(os.environ['HTTP_SERVERS'])
except KeyError:
    SERVERS = 3

class MyHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        """
        Default headers defined in separate function.
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
    
    def do_GET(self):
        """
        Logic to implement when HTTP GET on any URL is received.
        """
        # Balancing happens based on global counters
        global COUNTER, SERVERS
        
        # every next GET request goes to next server
        # servers name is docker container name (resoluton handled by bridge)
        j = COUNTER % SERVERS
        host = f"http://triznadm-http{j+1}"
        COUNTER += 1

        response = requests.get(host)
        self._set_response()
        self.wfile.write(response.text.encode('utf-8'))
        

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), f"Server Starts - {HOST_NAME}:{PORT_NUMBER}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), f"Server Stops - {HOST_NAME}:{PORT_NUMBER}")