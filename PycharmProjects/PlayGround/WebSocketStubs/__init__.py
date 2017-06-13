import socket

from VVStub import ServerProtocol
from autobahn.twisted.websocket import WebSocketServerFactory

from twisted.internet import reactor

# log.startLogging(sys.stdout)

factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
# factory = WebSocketServerFactory(u"ws://detector-dev.teletrax.com/detector")
factory.protocol = ServerProtocol
# factory.setProtocolOptions(maxConnections=2)

# note to self: if using putChild, the child must be bytes...

reactor.listenTCP(socket.IPPROTO_TCP,factory)
reactor.run()
print("Execution is returned here")