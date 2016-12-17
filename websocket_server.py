# -*- coding: utf-8 -*-

import os.path
from tornado import websocket, web, ioloop
import socket
import struct

# host = '192.168.100.110'
host = '127.0.0.1'
port = 13000
backlog = 10
bufsize = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

class WSHandler(websocket.WebSocketHandler):
    def open(self):
        print 'WebSocket opened'

    def on_message(self, message):
        sock.send(message)

        response = sock.recv(bufsize)
        self.write_message(response)
        print(response)

    def on_close(self):
        print('WebSocket closed')
        self.callback.stop()

application = web.Application(
    [(r'/', IndexHandler),
     (r'/ws', WSHandler)],
    static_path=os.path.join(os.path.dirname(__file__), "static"))

if __name__ == '__main__':
    application.listen(8888)
    ioloop.IOLoop.instance().start()
