#!/usr/bin/env python
# Answering Launcelot requests with a socketserver

## While server_multi.py creates all the workers up front so that they share
## the same listening socket, here we do the listening in the main thread and
## create one worker each time accept() returns a new client socket.

from SocketServer import ThreadingMixIn, TCPServer, BaseRequestHandler
import launcelot, server_simple, socket

class MyHandler(BaseRequestHandler):
    def handle(self):
        server_simple.handle_client(self.request)

class MyServer(ThreadingMixIn, TCPServer):
    allow_reuse_address = 1
    # address_family = socket.AF_INET6 # for when you need IPv6

server = MyServer(('', launcelot.PORT), MyHandler)
server.serve_forever()