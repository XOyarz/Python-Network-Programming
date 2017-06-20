#checking whether a hostname works both forwar and backward

import socket, sys
if len(sys.argv) != 2:
    print >>sys.stderr, 'usage: forward_reverse.py <hostname>'
    sys.exit(2)
hostname = sys.argv[1]

try:
    infolist = socket.getaddrinfo(
        hostname, 0, 0, socket.SOCK_STREAM, 0,
        socket.AI_ADDRCONFIG | socket.AI_V4MAPPED | socket.AI_CANONNAME,)
except socket.gaierror, e:
    print 'Forward name service failure:', e.args[1]
    sys.exit(1)

info = infolist[0]
canonical = info[3]
socketname = info[4]
ip = socketname[0]

if not canonical:
    print 'WARNING! The ip address', ip, 'has no reverse name'
    sys.exit(1)

print hostname, 'has IP address', ip
print ip, 'has the canonical hostname', canonical

# lowercase for case-insensitive comparison, and chop off hostnames

forward = hostname.lower().split('.')
reverse = canonical.lower().split('.')

if forward == reverse:
    print 'Wow the names agree completely'
    sys.exit(0)

#Truncate the domain names, which now look like ['www', 'mit', 'edu']
#to the same length and compare.

length = min(len(forward), len(reverse))
if (forward[-length:] == reverse[-length:]
    or (len(forward) == len(reverse)
        and forward[-length+1:] == reverse[-length+1:]
        and len(forward[-2]) > 2)): #avoid thinking '.co.uk' means a match!
    print 'The forward and reverse names ahave a lot in common!'
else:
    print 'Warning! The reverse name belongs to a different organization!'