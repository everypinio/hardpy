import http.server
import socketserver
import os

PORT = 8600
directory = os.path.join(os.getcwd(), 'examples/project/dialog_box/assets')
os.chdir(directory) 
Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
