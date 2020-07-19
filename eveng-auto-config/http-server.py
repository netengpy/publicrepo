
import http.server
import socketserver
import os

PORT = 80
Handler = http.server.SimpleHTTPRequestHandler
web_dir = os.path.join(os.path.dirname(__file__), 'atc-iol-initialcfgs')
os.chdir(web_dir)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("HTTP Server running on", PORT)
    httpd.serve_forever()


