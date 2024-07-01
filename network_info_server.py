from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import json

class NetworkInfoServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><head><title>Network Information</title></head>")
            self.wfile.write(b"<body>")
            self.wfile.write(b"<h1>Network Information</h1>")
            self.wfile.write(b"<p><strong>Hostname:</strong> " + socket.gethostname().encode('utf-8') + b"</p>")
            self.wfile.write(b"<p><strong>IP Address:</strong> " + self.get_ip_address().encode('utf-8') + b"</p>")
            self.wfile.write(b"<p><strong>Network Interfaces:</strong></p>")
            interfaces = json.dumps(self.get_network_interfaces(), indent=4).encode('utf-8')
            self.wfile.write(interfaces)
            self.wfile.write(b"</body></html>")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><head><title>Not Found</title></head>")
            self.wfile.write(b"<body><h1>404 - Not Found</h1></body></html>")

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def get_network_interfaces(self):
        interfaces = []
        for interface in socket.if_nameindex():
            interfaces.append({'index': interface[0], 'name': interface[1]})
        return interfaces

def run(server_class=HTTPServer, handler_class=NetworkInfoServer, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
