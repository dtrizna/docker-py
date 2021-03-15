from http.server import BaseHTTPRequestHandler,HTTPServer
import time
import redis
#from math import factorial
from scipy.special import factorial

HOST_NAME = ''
PORT_NUMBER = 80

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
        # Getting random key's value from Redis
        r = redis.Redis(host='triznadm-redis', port=6379, db=0)
        d = int(r.get(r.randomkey()).decode())
        
        # getting exact factiorial value of that
        f = factorial(d)
        # pretty printing exact factorial value in scientific notation
        # without that it's ~5000 character long integer
        # NOTE: cannot use native python's functionality for that
        # because it requires transforming of int to float and throws exception
        fl = list(str(f)[0:4])
        fl.insert(1,".")
        ppf = "".join(fl) + f"e+{len(str(f))-4}"

        # sending HTTP response
        self._set_response()
        self.wfile.write(f"Factorial of {d} = {ppf}\n".encode('utf-8'))

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), f"Server Starts - {HOST_NAME}:{PORT_NUMBER}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), f"Server Stops - {HOST_NAME}:{PORT_NUMBER}")