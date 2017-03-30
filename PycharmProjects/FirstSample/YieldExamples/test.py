import twisted
import txaio
from twisted.internet.defer import maybeDeferred
from twisted.internet.error import ConnectionDone, ConnectionAborted, ConnectionLost


from autobahn.twisted.util import transport_channel_id, peer2str
from autobahn.websocket import ConnectionDeny
from autobahn.websocket import protocol



class WebSocketAdapterProtocol(twisted.internet.protocol.Protocol):
    """
    Adapter class for Twisted WebSocket client and server protocols.
    """

    peer = u'<never connected>'

    log = txaio.make_logger()

    def connectionMade(self):
        # the peer we are connected to
        try:
            self.peer = peer2str(self.transport.getPeer())
        except AttributeError:
            # ProcessProtocols lack getPeer()
            self.peer = u'process:{}'.format(self.transport.pid)

        self._connectionMade()
        self.log.debug('Connection made to {peer}', peer=self.peer)

        # Set "Nagle"
        try:
            self.transport.setTcpNoDelay(self.tcpNoDelay)
        except:  # don't touch this! does not work: AttributeError, OSError
            # eg Unix Domain sockets throw Errno 22 on this
            pass

    def connectionLost(self, reason):
        if isinstance(reason.value, ConnectionDone):
            self.log.debug("Connection to/from {peer} was closed cleanly",
                           peer=self.peer)

        elif isinstance(reason.value, ConnectionAborted):
            self.log.debug("Connection to/from {peer} was aborted locally",
                           peer=self.peer)

        elif isinstance(reason.value, ConnectionLost):
            message = str(reason.value)
            if hasattr(reason.value, 'message'):
                message = reason.value.message
            self.log.debug(
                "Connection to/from {peer} was lost in a non-clean fashion: {message}",
                peer=self.peer,
                message=message,
            )

        # at least: FileDescriptorOverrun, ConnectionFdescWentAway - but maybe others as well?
        else:
            self.log.debug("Connection to/from {peer} lost ({error_type}): {error})",
                           peer=self.peer, error_type=type(reason.value), error=reason.value)

        self._connectionLost(reason)

    def dataReceived(self, data):
        self._dataReceived(data)

    def _closeConnection(self, abort=False):
        if abort and hasattr(self.transport, 'abortConnection'):
            self.transport.abortConnection()
        else:
            # e.g. ProcessProtocol lacks abortConnection()
            self.transport.loseConnection()

    def _onOpen(self):
        self.onOpen()

    def _onMessageBegin(self, isBinary):
        self.onMessageBegin(isBinary)

    def _onMessageFrameBegin(self, length):
        self.onMessageFrameBegin(length)

    def _onMessageFrameData(self, payload):
        self.onMessageFrameData(payload)

    def _onMessageFrameEnd(self):
        self.onMessageFrameEnd()

    def _onMessageFrame(self, payload):
        self.onMessageFrame(payload)

    def _onMessageEnd(self):
        self.onMessageEnd()

    def _onMessage(self, payload, isBinary):
        self.onMessage(payload, isBinary)

    def _onPing(self, payload):
        self.onPing(payload)

    def _onPong(self, payload):
        self.onPong(payload)

    def _onClose(self, wasClean, code, reason):
        self.onClose(wasClean, code, reason)

    def registerProducer(self, producer, streaming):
        """
        Register a Twisted producer with this protocol.

        :param producer: A Twisted push or pull producer.
        :type producer: object
        :param streaming: Producer type.
        :type streaming: bool
        """
        self.transport.registerProducer(producer, streaming)



class WebSocketServerProtocol(WebSocketAdapterProtocol, protocol.WebSocketServerProtocol):
    """
    Base class for Twisted-based WebSocket server protocols.
    """

    def _onConnect(self, request):
        # onConnect() will return the selected subprotocol or None
        # or a pair (protocol, headers) or raise an HttpException
        res = maybeDeferred(self.onConnect, request)

        res.addCallback(self.succeedHandshake)

        def forwardError(failure):
            if failure.check(ConnectionDeny):
                return self.failHandshake(failure.value.reason, failure.value.code)
            else:
                self.log.debug("Unexpected exception in onConnect ['{failure.value}']", failure=failure)
                return self.failHandshake("Internal server error: {}".format(failure.value), ConnectionDeny.INTERNAL_SERVER_ERROR)

        res.addErrback(forwardError)

    def get_channel_id(self, channel_id_type=u'tls-unique'):
        """
        Implements :func:`autobahn.wamp.interfaces.ITransport.get_channel_id`
        """
        return transport_channel_id(self.transport, is_server=True, channel_id_type=channel_id_type)
