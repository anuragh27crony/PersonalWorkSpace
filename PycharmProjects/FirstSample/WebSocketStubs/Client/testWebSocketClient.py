import json

from websocket import create_connection

ws = create_connection("ws://detector-dev.teletrax.com/detector")
print("Sending 'Hello, World'...")
register_message = "{'data':{'maxTransferQueueSize':10,'channels':[{'index':1,'verificationVideo':{'enabled':true}},{'index':2,'verificationVideo':{'enabled':true}},{'index':3,'verificationVideo':{'enabled':true}},{'index':4,'verificationVideo':{'enabled':true}},{'index':5,'verificationVideo':{'enabled':true}},{'index':6,'verificationVideo':{'enabled':true}},{'index':7,'verificationVideo':{'enabled':true}},{'index':8,'verificationVideo':{'enabled':true}},{'index':9,'verificationVideo':{'enabled':true}},{'index':10,'verificationVideo':{'enabled':true}},{'index':11,'verificationVideo':{'enabled':true}},{'index':12,'verificationVideo':{'enabled':true}},{'index':13,'verificationVideo':{'enabled':true}},{'index':14,'verificationVideo':{'enabled':true}},{'index':15,'verificationVideo':{'enabled':true}},{'index':16,'verificationVideo':{'enabled':true}},{'index':17,'verificationVideo':{'enabled':true}},{'index':18,'verificationVideo':{'enabled':true}},{'index':19,'verificationVideo':{'enabled':true}},{'index':20,'verificationVideo':{'enabled':true}},{'index':21,'verificationVideo':{'enabled':true}},{'index':22,'verificationVideo':{'enabled':true}},{'index':23,'verificationVideo':{'enabled':true}},{'index':24,'verificationVideo':{'enabled':true}},{'index':25,'verificationVideo':{'enabled':true}},{'index':26,'verificationVideo':{'enabled':true}}],'detectorId':'0D02','version':'1.0'},'message':{'id':'8d4b8055-6deb-4bcf-966f-54b5e3132afd','type':'videoProviderRegisterRequest'}}"
ws.send(register_message)
print("Sent")

while True:
    result = ws.recv()
    json_response = json.loads(result)
    print("Received '%s'" % result)
    id = json_response.get("message").get("id")
    # if json_response.get("message").get("type") == "videoUploadRequest":
    #     msg_response = "{'data':{'fragments':[{'startDateTime':'2017-02-12T14:26:00Z','size':679675,'location':'d:\\civolution\\Data\\VerificationVideo\\02\\170212\\14\\WcT0D02170212142600_02.mp4','endDateTime':'2017-02-12T14:27:00Z'},{'startDateTime':'2017-02-12T14:27:00Z','size':663928,'location':'d:\\civolution\\Data\\VerificationVideo\\02\\170212\\14\\WcT0D02170212142700_02.mp4','endDateTime':'2017-02-12T14:28:00Z'},{'startDateTime':'2017-02-12T14:28:00Z','size':630245,'location':'d:\\civolution\\Data\\VerificationVideo\\02\\170212\\14\\WcT0D02170212142800_02.mp4','endDateTime':'2017-02-12T14:29:00Z'}]},'success':true,'message':{'id':'" + id + "','type':'videoUploadReply'}}"
    #     ws.send(json.dumps(msg_response))
    # if json_response.get("message").get("type") == "videoRecordingCapacityRequest":
    #     msg_response = "{'data':{'channels':[{'newestDateTime':'2017-03-13T10:36:00Z','index':1,'oldestDateTime':'2017-02-08T14:19:51Z'},{'newestDateTime':'2017-03-13T10:36:00Z','index':2,'oldestDateTime':'2017-02-08T14:19:47Z'}],'totalStorageCapacity':2047.9980430603027,'totalAvailableStorageCapacity':633.3623542785645,'totalAverageStorageCapacityPerDay':62.840005561709404},'success':true,'message':{'id':'" + id + "','type':'videoRecordingCapacityReply'}}"
    #     ws.send(json.dumps(msg_response))
    # if json_response.get("message").get("type") == "videoTransferRequest":
    #     msg_response = "{'success':true,'message':{'id':'" + id + "','type':'videoTransferReply'}}"
    #     ws.send(json.dumps(msg_response))
    print("Response Sent ")
