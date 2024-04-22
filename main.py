from socketserver import TCPServer

from server import MyTCPHandler, ThreadedTCPServer


HOST = 'localhost', 3344
TCPServer.allow_reuse_address = True
with ThreadedTCPServer(HOST, MyTCPHandler) as server:
    server.serve_forever()
