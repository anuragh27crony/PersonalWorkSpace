from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory

PORT = 9000


class LineServer(LineReceiver):
    def connectionMade(self):
        """
        Overridden event handler that is called when a connection to the
        server was made
        """
        print "server received a connection!"

    def connectionLost(self, reason):
        """
        Overridden event handler that is called when the connection
        between the server and the client is lost
        @param reason: Reason for loss of connection
        """
        print "Connection lost"
        print reason

    def lineReceived(self, data):
        """
        Overridden event handler for when a line of data is
        received from client
        @param data: The data received from the client
        """
        print 'in lineReceived'
        print 'data => ' + data


class ServerFactory(Factory):
    protocol = LineServer


if __name__ == '__main__':
    factory = ServerFactory()
    reactor.listenTCP(9000, factory)
    reactor.run()