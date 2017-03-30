from autobahn.twisted.websocket import WebSocketServerProtocol
import json

from datetime import datetime
from twisted.internet import reactor


class ServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        __is_request_handled = False
        if isBinary:
            print("Binary message received: {} bytes".format(len(payload)))
        else:
            incoming_message = json.loads(payload.decode('utf8'))
            print("Text message received: {}".format(payload.decode('utf8')))
            message_type = incoming_message.get("message").get("type")

            # Parse VV Register Request & Return a success Reply.
            if message_type == "videoProviderRegisterRequest":
                reply = send_register_reply()
                self.sendMessage(json.dumps(reply), isBinary)
                __is_request_handled = True

                # Send Request for Video Upload
                detector_id = "0D02"
                if incoming_message.get("data"):
                    detector_id = incoming_message.get("data").get("detectorId")
                print(datetime.now().isoformat(' '))
                video_upload_request = request_video_upload(detector_id, start_time=datetime.now().isoformat(' '),
                                                            end_time=datetime.now().isoformat(' '))
                self.sendMessage(json.dumps(video_upload_request), False)

            if message_type == "videoUploadReply" and incoming_message.get("success"):
                validate_video_upload_reply(incoming_message=incoming_message)
        print("Entered here")
        if __is_request_handled:
            self.sendCloseFrame(code=1006)
            # self.terminate_connection()

            # def sendMessageFrame(self, payload, sync=False):
            #     pass
            # def terminate_connection(self):
            #     reactor.callLater(1, reactor.stop)


def send_register_reply(msg_id="", is_success=False):
    reply_message = {"type": "videoProviderRegisterReply"}  # Fetch from a dict objs ReplyTypes
    reply_message.update({"id": msg_id})
    reply = {"success": is_success, "message": reply_message}
    return reply


def request_video_upload(detector_id="", channel_index="1", start_time="", end_time=""):
    request_meta = {"type": "videoUploadRequest", "id": "dcbaedf5-3e13-4807-b8ed-5c6848f88f6d"}
    request_data = {"detectorId": detector_id, "type": "verificationVideo", "index": channel_index,
                    "startDateTime": start_time, "endDateTime": end_time}
    return {"message": request_meta, "data": request_data}


def validate_video_upload_reply(incoming_message):
    fragments = incoming_message.get("data").get("fragments")

    for video_fragment in fragments:
        print(type(video_fragment))
