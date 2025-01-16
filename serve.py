import http.server
import socketserver
import argparse
import webbrowser
from urllib.parse import quote

# Create argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--api_url', default='http://localhost:5000/api/chat', 
                   help='Backend API URL')
parser.add_argument('--port', type=int, default=8000,
                   help='Port to serve on')

args = parser.parse_args()

# Start the server
Handler = http.server.SimpleHTTPRequestHandler
port = args.port

with socketserver.TCPServer(("", port), Handler) as httpd:
    print(f"Serving at port {port}")
    # Open browser with the API URL parameter
    webbrowser.open(f'http://localhost:{port}/frontend?api_url={quote(args.api_url)}')
    httpd.serve_forever() 