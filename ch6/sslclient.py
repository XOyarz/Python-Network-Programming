#!/usr/bin/env python
#using ssl to protect a socket

import os, socket, ssl, sys
from backports.ssl_match_hostname import match_hostname, CertificateError

try:
    script_name, hostname = sys.argv
except ValueError:
    print >>sys.stderr, 'usage: sslclient.py <hostname>'
    sys.exit(2)

#connect as usual with a socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((hostname, 443))

#next, turn teh socket over to the ssl library

ca_certs_path = os.path.join(os.path.dirname(script_name), 'certfiles.crt')
sslsock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv3,
                          cert_reqs=ssl.CERT_REQUIRED, ca_certs=ca_certs_path)

#Does the cert that the server proffered really match the hostname
#to which we are trying to connect? Check!

try:
    match_hostname(sslsock.getpeercert(), hostname)
except CertificateError, ce:
    print 'Certificate error', str(ce)
    sys.exit(1)

#from here on, our `sslsock` works like a normal socket

sslsock.sendall('GET / HTTP/1.0\r\n\r\n')
result = sslsock.makefile().read() #quick way to read until EOF
sslsock.close()
print 'The document https://%s/ is %d bytes long' % (hostname, len(result))