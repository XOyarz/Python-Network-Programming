#!/usr/bin/env
# Using Twisted to serve Launcelot users

from twisted.internet.protocol import Protocol, ServerFactory
from twisted.internet import reactor
import launcelot

class Launcelot(Protocol):
    def connectionMade(self):
        self.question = ''

    def dataReceived(self, data):
        self.question += data
        if self.question.endswith('?'):
            self.transport.write(dict(launcelot.qa)[self.question])
            self.question = ''

factory = ServerFactory()
factory.protocol = Launcelot
reactor.listenTCP(1060, factory)
reactor.run()