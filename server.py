import http.server, socketserver, socket, select

class Proxy(http.server.SimpleHTTPRequestHandler):
    def do_CONNECT(self):
        address = self.path.split(":", 1)
        address[1] = int(address[1])
        try:
            s = socket.create_connection(address, timeout=10)
        except:
            self.send_error(502); return
        self.send_response(200, 'Connection Established')
        self.end_headers()
        conns = [self.connection, s]
        while True:
            r_ready, _, _ = select.select(conns, [], [], 10)
            if not r_ready: break
            for r in r_ready:
                other = conns[1] if r is conns[0] else conns[0]
                data = r.recv(8192)
                if not data: return
                other.sendall(data)

PORT = 8888
print(f"Proxy ON na porta {PORT}")
socketserver.ThreadingTCPServer(("", PORT), Proxy).serve_forever()
