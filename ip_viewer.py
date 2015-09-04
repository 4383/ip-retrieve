#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost

nginx restriction :
    location / {
    allow 192.168.1.1/24;
    allow 127.0.0.1;
    deny 192.168.1.2;
    deny all;
}
"""
from http.server import SimpleHTTPRequestHandler, HTTPServer


class IPServer(SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        response = self.client_address[0]
        response = self.headers["X-Real-IP"]
        self.wfile.write(response.encode("utf-8"))

    def do_HEAD(self):
        self._set_headers()


def run(server_class=HTTPServer, handler_class=IPServer, port=6666):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
