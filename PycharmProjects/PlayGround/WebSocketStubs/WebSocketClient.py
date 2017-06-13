from Queue import Queue

from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory


class MyClientProtocol(WebSocketClientProtocol):
    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onPong(self, payload):
        pass;
    def onOpen(self):
        print("WebSocket connection open.")

        def hello():
            q = Queue()
            q.put("Testing is fun")
            self.sendMessage(u"Hello, world!".encode('utf8'))
            # self.sendMessage(b"\x00\x01\x03\x04", isBinary=True)
            # self.factory.reactor.callLater(1, hello)

        # start sending messages every second ..
        hello()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':
    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000")
    factory.protocol = MyClientProtocol

    reactor.connectTCP("127.0.0.1", 9000, factory)
    reactor.run()



factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
factory.protocol = ServerProtocol
# factory.setProtocolOptions(maxConnections=2)

# note to self: if using putChild, the child must be bytes...

