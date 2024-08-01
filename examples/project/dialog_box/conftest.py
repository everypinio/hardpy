import pytest
import http.server
import socketserver
import os

PORT = 8600


@pytest.fixture(scope="session")
def http_server():
    directory = os.path.join(os.getcwd(), 'examples/project/dialog_box/assets')
    os.chdir(directory) 
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
        yield httpd
