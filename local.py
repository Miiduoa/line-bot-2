#!/usr/bin/env python3
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from api.index import handle_request

PORT = int(os.environ.get('PORT', 3000))

class LocalHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """處理 GET 請求"""
        response = handle_request('', self.path, 'GET', dict(self.headers))
        self.send_response(response.get('statusCode', 200))
        for key, value in response.get('headers', {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response.get('body', '').encode('utf-8'))
    
    def do_POST(self):
        """處理 POST 請求"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ''
        
        response = handle_request(body, self.path, 'POST', dict(self.headers))
        
        self.send_response(response.get('statusCode', 200))
        for key, value in response.get('headers', {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response.get('body', '').encode('utf-8'))

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', PORT), LocalHandler)
    print(f'Local development server running on port {PORT}')
    print(f'Try http://localhost:{PORT}/ to check if it is running')
    print(f'Use ngrok to expose http://localhost:{PORT}/callback as LINE webhook URL')
    server.serve_forever() 