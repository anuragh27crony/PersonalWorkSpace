import websocket
import thread



def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print
    "### closed ###"


def on_open(ws):
    register = "{'data':{'maxTransferQueueSize':10,'channels':[{'index':1,'verificationVideo':{'enabled':true}},{'index':2,'verificationVideo':{'enabled':true}},{'index':3,'verificationVideo':{'enabled':true}},{'index':4,'verificationVideo':{'enabled':true}},{'index':5,'verificationVideo':{'enabled':true}},{'index':6,'verificationVideo':{'enabled':true}},{'index':7,'verificationVideo':{'enabled':true}},{'index':8,'verificationVideo':{'enabled':true}},{'index':9,'verificationVideo':{'enabled':true}},{'index':10,'verificationVideo':{'enabled':true}},{'index':11,'verificationVideo':{'enabled':true}},{'index':12,'verificationVideo':{'enabled':true}},{'index':13,'verificationVideo':{'enabled':true}},{'index':14,'verificationVideo':{'enabled':true}},{'index':15,'verificationVideo':{'enabled':true}},{'index':16,'verificationVideo':{'enabled':true}},{'index':17,'verificationVideo':{'enabled':true}},{'index':18,'verificationVideo':{'enabled':true}},{'index':19,'verificationVideo':{'enabled':true}},{'index':20,'verificationVideo':{'enabled':true}},{'index':21,'verificationVideo':{'enabled':true}},{'index':22,'verificationVideo':{'enabled':true}},{'index':23,'verificationVideo':{'enabled':true}},{'index':24,'verificationVideo':{'enabled':true}},{'index':25,'verificationVideo':{'enabled':true}},{'index':26,'verificationVideo':{'enabled':true}}],'detectorId':'0D02','version':'1.0'},'message':{'id':'8d4b8055-6deb-4bcf-966f-54b5e3132afd','type':'videoProviderRegisterRequest'}}"
    ws.send(register)

    def run(*args):
        print(ws.recv())

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://detector-dev.teletrax.com/detector",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
