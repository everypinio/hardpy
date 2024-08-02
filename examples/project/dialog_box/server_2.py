import http.server
import socketserver
import os
import threading
import time

# PORT = 8600
# directory = os.path.join(os.getcwd(), 'examples/project/dialog_box/assets')
# os.chdir(directory) 
# Handler = http.server.SimpleHTTPRequestHandler

# httpd = socketserver.TCPServer(("", PORT), Handler)

# print("serving at port", PORT)
# httpd.serve_forever()

PORT = 8600
directory = os.path.join(os.getcwd(), 'examples/project/dialog_box/assets')
os.chdir(directory)
handler = http.server.SimpleHTTPRequestHandler

def run_server(stop_event):
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("serving at port", PORT)
        while not stop_event.is_set():
            httpd.handle_request()

stop_event = threading.Event()

server_thread = threading.Thread(target=run_server, args=(stop_event,))
server_thread.start()

time.sleep(5)

stop_event.set()

server_thread.join()