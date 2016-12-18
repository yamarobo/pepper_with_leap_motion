# -*- coding: utf-8 -*-

import socket
import select

def main():
    #change here to specify the address of this server process
    host = '192.168.100.110'
    # host = '127.0.0.1'
    port = 13000
    backlog = 10
    bufsize = 4096
    state = 'default'

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    readfds = set([server_sock])
    try:
        server_sock.bind((host, port))
        server_sock.listen(backlog)

        while True:
            rready, wready, xready = select.select(readfds, [], [])
            for sock in rready:
                if sock is server_sock:
                    conn, address = server_sock.accept()
                    print("new connection established")
                    readfds.add(conn)
                else:
                    msg = sock.recv(bufsize)
                    if len(msg) == 0:
                        sock.close()
                        print("disconnected")
                        readfds.remove(sock)
                    else:
                        print(msg)
                        #sock.send(msg)
                        if msg != 'get_action':
                            state = msg
                        sock.send(state)
                        if msg == 'get_action':
                            state = 'default'
    finally:
        for sock in readfds:
            sock.close()

    return

if __name__ == '__main__':
    main()
