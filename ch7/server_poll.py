#!/usr/bin/env python
#even-driven approach to serving several clients with poll()

## poll() is like recv(), only recv() waits on one single client, while
## poll() can wait on hundreds of clients, and return to whichever one
## shows any activity.We tell poll() wwhich sockets interest us, and
## whether we want to read or write from them. Both poll() and recv() are
## blocking calls.

## authors recommend not coding down to this level, because it's very messy.
## Instead, usa an even-driven framework, which does all the work for you. Twisted??

import launcelot
import select

listen_sock = launcelot.setup()
sockets = { listen_sock.fileno(): listen_sock}
requests = {}
responses = {}

poll = select.poll()
poll.register(listen_sock, select.POLLIN)

while True:
    for fd, event in poll.poll():
        sock = sockets[fd]
        #removed closed sockets from our list.
        if event & (select.POLLHUP | select.POLLERR | select.POLLNVAL):
            poll.unregister(fd)
            del sockets[fd]
            requests.pop(sock, None)
            responses.pop(sock, None)

        #accept connections from new sockets.
        elif sock is listen_sock:
            newsock, sockname = sock.accept()
            newsock.setblocking(False) # allow this socket to block the event loop = FALSE
            fd = newsock.fileno()
            sockets[fd] = newsock
            poll.register(fd, select.POLLIN)
            requests[newsock] = ''

        #Collect incoming data until it forms a question
        elif event & select.POLLIN: #accept incoming data
            data = sock.recv(4096) #receive incoming data...
            if not data: #EOF
                sock.close() #makes POLLNVAL happen next time
                continue
            requests[sock] += data
            if '?' in requests[sock]: # ...until we see a '?'
                question = requests.pop(sock)
                answer = dict(launcelot.qa)[question] #look up the answer to the received q
                poll.modify(sock, select.POLLOUT) #POLLOUT, because now we want to send data on this sock
                responses[sock] = answer # get answer ready to be sent

        #send out pieces of each reply until they are all sent
        elif event & select.POLLOUT:
            response = responses.pop(sock)
            n = sock.send(response)
            if n < len(response):
                responses[sock] = response [n:]
            else:
                poll.modify(sock, select.POLLIN) # once done sending our answer, switch back to listening on this sock
                requests[sock] = ''