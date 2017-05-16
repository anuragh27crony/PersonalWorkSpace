import socket

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import json

from multiprocessing import Queue

from twisted.internet import reactor


class ServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        self.message_queue = Queue()
        self.request_host = request.host
        print("Client connecting: {}".format(request.peer))

    def onPing(self, payload):
        pass;

    def onOpen(self):
        print("WebSocket connection open.")
        register_message="{'data':{'maxTransferQueueSize':10,'channels':[{'index':1,'verificationVideo':{'enabled':true}},{'index':2,'verificationVideo':{'enabled':true}},{'index':3,'verificationVideo':{'enabled':true}},{'index':4,'verificationVideo':{'enabled':true}},{'index':5,'verificationVideo':{'enabled':true}},{'index':6,'verificationVideo':{'enabled':true}},{'index':7,'verificationVideo':{'enabled':true}},{'index':8,'verificationVideo':{'enabled':true}},{'index':9,'verificationVideo':{'enabled':true}},{'index':10,'verificationVideo':{'enabled':true}},{'index':11,'verificationVideo':{'enabled':true}},{'index':12,'verificationVideo':{'enabled':true}},{'index':13,'verificationVideo':{'enabled':true}},{'index':14,'verificationVideo':{'enabled':true}},{'index':15,'verificationVideo':{'enabled':true}},{'index':16,'verificationVideo':{'enabled':true}},{'index':17,'verificationVideo':{'enabled':true}},{'index':18,'verificationVideo':{'enabled':true}},{'index':19,'verificationVideo':{'enabled':true}},{'index':20,'verificationVideo':{'enabled':true}},{'index':21,'verificationVideo':{'enabled':true}},{'index':22,'verificationVideo':{'enabled':true}},{'index':23,'verificationVideo':{'enabled':true}},{'index':24,'verificationVideo':{'enabled':true}},{'index':25,'verificationVideo':{'enabled':true}},{'index':26,'verificationVideo':{'enabled':true}}],'detectorId':'0D08','version':'1.0'},'message':{'id':'8d4b8055-6deb-4bcf-966f-54b5e3132afd','type':'videoProviderRegisterRequest'}}"
        self.sendMessage(json.dumps(register_message), isBinary=False)

    def onMessage(self, payload, isBinary):
        print(isBinary)
        if isBinary:
            print("Binary message received: {} bytes".format(len(payload)))
            print(payload)
        else:
            self.message_queue.put(payload.decode('utf8'))
            incoming_message = json.loads(payload.decode('utf8'))
            print("Text message received: {}".format(payload.decode('utf8')))
            # # self.sendFrame(opcode=1)
            # # self.sendFrame(opcode=2)
            # message_details = incoming_message.get("message")
            # message_type = message_details.get("type")
            #
            # message_data = incoming_message.get("data")
            # if message_data:
            #     detector_id = message_data.get("detectorId")
            #
            # if message_type == "videoProviderRegisterRequest":
            #     data = {"message": {
            #         "type": "videoRecordingCapacityRequest",
            #         "id": "dcbaedf5-3e13-4807-b8ed-5c6848f88f6d"
            #     },
            #         "data": {
            #             "type": "verificationVideo"
            #         }
            #     }
            #     self.sendMessage(json.dumps(data), isBinary)
            #     # self.send
            #     # self.sendFrame(opcode=1)
            #     # self.sendFrame(opcode=2)
            #     # # self.sendFrame(opcode=3)
            #     # for i in range(100, 140, 1):
            #     #     self.sendFrame(opcode=i)
            #     print("Now Closse")
            #     # self.sendCloseFrame(code=1004)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))


factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
# factory = WebSocketServerFactory(u"ws://detector-dev.teletrax.com/detector")
factory.protocol = ServerProtocol
# factory.setProtocolOptions(maxConnections=2)

# note to self: if using putChild, the child must be bytes...

reactor.listenTCP(socket.IPPROTO_TCP,factory)
reactor.run()
print("Execution is returned here")