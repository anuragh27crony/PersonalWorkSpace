from autobahn.twisted.websocket import WebSocketServerProtocol
import json

from multiprocessing import Queue

class ServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        self.message_queue = Queue()
        self.request_host = request.host
        print("Client connecting: {}".format(request.peer))

    def onPing(self, payload):
        pass;

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        print(isBinary)
        if isBinary:
            print("Binary message received: {} bytes".format(len(payload)))
            print(payload)
        else:
            self.message_queue.put(payload.decode('utf8'))
            incoming_message = json.loads(payload.decode('utf8'))
            print("Text message received: {}".format(payload.decode('utf8')))

            message_details = incoming_message.get("message")
            message_type = message_details.get("type")

            message_data = incoming_message.get("data")
            if message_data:
                detector_id = message_data.get("detectorId")

            if message_type == "videoProviderRegisterRequest":
                data = {"message": {
                    "type": "videoRecordingCapacityRequest",
                    "id": "dcbaedf5-3e13-4807-b8ed-5c6848f88f6d"
                },
                    "data": {
                        "type": "verificationVideo"
                    }
                }
                self.sendMessage(json.dumps(data), isBinary)


    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))


if __name__ == '__main__':
    from autobahn.twisted.websocket import WebSocketServerFactory

    from twisted.internet import reactor

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = ServerProtocol
    # log.startLogging(sys.stdout)

    reactor.listenTCP(9000, factory)
    reactor.run()
    print("Execution is returned here")
