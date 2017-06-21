#!/usr/bin/env python
#Simple Launcelot client that asks three questions then disconnects.

import socket, sys, launcelot

def client(hostname, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.sendall(launcelot.qa[0][0])
    answer1 = launcelot.recv_until(s, '.') #answers end with '.'
    s.sendall(launcelot.qa[1][0])
    answer2 = launcelot.recv_until(s, '.')
    s.sendall(launcelot.qa[2][0])
    answer3 = launcelot.recv_until(s, '.')
    s.close()
    print answer1
    print answer2
    print answer3

if __name__ == '__main__':
    if not 2 <= len(sys.argv) <= 3:
        print >>sys.stderr, 'usage:client.py hostname [port]'
        sys.exit(2)
    port = int(sys.argv[2] if len(sys.argv) > 2 else launcelot.PORT)
    client(sys.argv[1], port)
    