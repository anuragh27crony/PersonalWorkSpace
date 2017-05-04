import requests
import json
import base64

from operator import itemgetter


def encode_ceco(ceco_file_path=None, encoded_file_output=None):
    with open(ceco_file_path, "rb") as ceco_file:
        encoded_string = base64.b64encode(ceco_file.read())

    if encoded_file_output is not None:
        with open(encoded_file_output, "w") as write_file:
            write_file.write(encoded_string)

    return encoded_string


encode_ceco(ceco_file_path="D:\\CecoComparision\\4.4(28-Apr-08Hr)\\WcD0D001704280600_01.ce",
            encoded_file_output="D:\\CecoComparision\\4.4(28-Apr-08Hr)\\base64\\Base641704280600_01.txt")


def read_fps_identify_results(json_string):
    json_obj = json.loads(json_string)
    sorted(json_obj.get('results'), key=itemgetter('candidateStartOffset'))

    print(json.dumps(json_obj))
    return json.dumps(json_obj)


read_fps_identify_results(
    json_string="{ \"results\": [ { \"id\": \"2016042806\", \"metadata\": \"4.32016042806\", \"candidateStartOffset\": 0, \"candidateEndOffset\": 51201, \"candidateStartUtc\": \"2017-04-28T05:59:43.422Z\", \"candidateEndUtc\": \"2017-04-28T06:00:34.623Z\", \"referenceStartUtc\": \"2017-04-28T06:10:01.340Z\", \"referenceEndUtc\": \"2017-04-28T06:10:52.540Z\", \"referenceNextUtc\": \"2017-04-28T06:29:43.667Z\", \"type\": \"feed\", \"berAverage\": 0.0893128357975525, \"transform\": \"none\" }, { \"id\": \"2016042806\", \"metadata\": \"4.32016042806\", \"candidateStartOffset\": 0, \"candidateEndOffset\": 121019, \"candidateStartUtc\": \"2017-04-28T05:59:43.422Z\", \"candidateEndUtc\": \"2017-04-28T06:01:44.441Z\", \"referenceStartUtc\": \"2017-04-28T05:59:43.358Z\", \"referenceEndUtc\": \"2017-04-28T06:01:44.376Z\", \"referenceNextUtc\": \"2017-04-28T06:29:43.667Z\", \"type\": \"feed\", \"berAverage\": 0.09266226293421038, \"transform\": \"none\" }, { \"id\": \"2016042806\", \"metadata\": \"4.32016042806\", \"candidateStartOffset\": 232728, \"candidateEndOffset\": 269964, \"candidateStartUtc\": \"2017-04-28T06:03:36.150Z\", \"candidateEndUtc\": \"2017-04-28T06:04:13.386Z\", \"referenceStartUtc\": \"2017-04-28T06:13:54.067Z\", \"referenceEndUtc\": \"2017-04-28T06:14:31.303Z\", \"referenceNextUtc\": \"2017-04-28T06:29:43.667Z\", \"type\": \"feed\", \"berAverage\": 0.10375993330128454, \"transform\": \"none\" }, { \"id\": \"2016042806\", \"metadata\": \"4.32016042806\", \"candidateStartOffset\": 274618, \"candidateEndOffset\": 279273, \"candidateStartUtc\": \"2017-04-28T06:04:18.040Z\", \"candidateEndUtc\": \"2017-04-28T06:04:22.695Z\", \"referenceStartUtc\": \"2017-04-28T06:14:35.958Z\", \"referenceEndUtc\": \"2017-04-28T06:14:40.613Z\", \"referenceNextUtc\": \"2017-04-28T06:29:43.667Z\", \"type\": \"feed\", \"berAverage\": 0.109375, \"transform\": \"none\" }, { \"id\": \"2016042806\", \"metadata\": \"4.32016042806\", \"candidateStartOffset\": 744727, \"candidateEndOffset\": 884363, \"candidateStartUtc\": \"2017-04-28T06:12:08.149Z\", \"candidateEndUtc\": \"2017-04-28T06:14:27.785Z\", \"referenceStartUtc\": \"2017-04-28T06:12:08.085Z\", \"referenceEndUtc\": \"2017-04-28T06:14:27.722Z\", \"referenceNextUtc\": \"2017-04-28T06:29:43.667Z\", \"type\": \"feed\", \"berAverage\": 0.12008272469926444, \"transform\": \"none\" }, { \"id\": \"2016042806\", \"metadata\": \"4.32016042806\", \"candidateStartOffset\": 274618, \"candidateEndOffset\": 740072, \"candidateStartUtc\": \"2017-04-28T06:04:18.040Z\", \"candidateEndUtc\": \"2017-04-28T06:12:03.494Z\", \"referenceStartUtc\": \"2017-04-28T06:04:17.976Z\", \"referenceEndUtc\": \"2017-04-28T06:12:03.431Z\", \"referenceNextUtc\": \"2017-04-28T06:29:43.667Z\", \"type\": \"feed\", \"berAverage\": 0.12124900333248387, \"transform\": \"none\" }, { \"id\": \"2016042806\", \"metadata\": \"4.32016042806\", \"candidateStartOffset\": 130328, \"candidateEndOffset\": 269964, \"candidateStartUtc\": \"2017-04-28T06:01:53.750Z\", \"candidateEndUtc\": \"2017-04-28T06:04:13.386Z\", \"referenceStartUtc\": \"2017-04-28T06:01:53.685Z\", \"referenceEndUtc\": \"2017-04-28T06:04:13.322Z\", \"referenceNextUtc\": \"2017-04-28T06:29:43.667Z\", \"type\": \"feed\", \"berAverage\": 0.12485432834376162, \"transform\": \"none\" }, { \"id\": \"2016042806\", \"metadata\": \"4.32016042806\", \"candidateStartOffset\": 851781, \"candidateEndOffset\": 884363, \"candidateStartUtc\": \"2017-04-28T06:13:55.203Z\", \"candidateEndUtc\": \"2017-04-28T06:14:27.785Z\", \"referenceStartUtc\": \"2017-04-28T06:24:13.067Z\", \"referenceEndUtc\": \"2017-04-28T06:24:45.631Z\", \"referenceNextUtc\": \"2017-04-28T06:29:43.667Z\", \"type\": \"feed\", \"berAverage\": 0.1291846584868902, \"transform\": \"none\" }, { \"id\": \"2016042806\", \"metadata\": \"4.32016042806\", \"candidateStartOffset\": 274618, \"candidateEndOffset\": 279273, \"candidateStartUtc\": \"2017-04-28T06:04:18.040Z\", \"candidateEndUtc\": \"2017-04-28T06:04:22.695Z\", \"referenceStartUtc\": \"2017-04-28T06:24:53.885Z\", \"referenceEndUtc\": \"2017-04-28T06:24:58.540Z\", \"referenceNextUtc\": \"2017-04-28T06:29:43.667Z\", \"type\": \"feed\", \"berAverage\": 0.129395, \"transform\": \"none\" }, { \"id\": \"2016042806\", \"metadata\": \"4.32016042806\", \"candidateStartOffset\": 232728, \"candidateEndOffset\": 269964, \"candidateStartUtc\": \"2017-04-28T06:03:36.150Z\", \"candidateEndUtc\": \"2017-04-28T06:04:13.386Z\", \"referenceStartUtc\": \"2017-04-28T06:24:11.994Z\", \"referenceEndUtc\": \"2017-04-28T06:24:49.231Z\", \"referenceNextUtc\": \"2017-04-28T06:29:43.667Z\", \"type\": \"feed\", \"berAverage\": 0.14105275288758765, \"transform\": \"none\" }, { \"id\": \"2016042806\", \"metadata\": \"4.32016042806\", \"candidateStartOffset\": 847127, \"candidateEndOffset\": 884363, \"candidateStartUtc\": \"2017-04-28T06:13:50.549Z\", \"candidateEndUtc\": \"2017-04-28T06:14:27.785Z\", \"referenceStartUtc\": \"2017-04-28T06:03:32.503Z\", \"referenceEndUtc\": \"2017-04-28T06:04:09.740Z\", \"referenceNextUtc\": \"2017-04-28T06:29:43.667Z\", \"type\": \"feed\", \"berAverage\": 0.14208535351796414, \"transform\": \"none\" }, { \"id\": \"2016042806\", \"metadata\": \"4.32016042806\", \"candidateStartOffset\": 614399, \"candidateEndOffset\": 679563, \"candidateStartUtc\": \"2017-04-28T06:09:57.821Z\", \"candidateEndUtc\": \"2017-04-28T06:11:02.985Z\", \"referenceStartUtc\": \"2017-04-28T06:20:15.667Z\", \"referenceEndUtc\": \"2017-04-28T06:21:20.849Z\", \"referenceNextUtc\": \"2017-04-28T06:29:43.667Z\", \"type\": \"feed\", \"berAverage\": 0.15415978176122358, \"transform\": \"none\" }, { \"id\": \"2016042806\", \"metadata\": \"4.32016042806\", \"candidateStartOffset\": 0, \"candidateEndOffset\": 121019, \"candidateStartUtc\": \"2017-04-28T05:59:43.422Z\", \"candidateEndUtc\": \"2017-04-28T06:01:44.441Z\", \"referenceStartUtc\": \"2017-04-28T06:20:19.267Z\", \"referenceEndUtc\": \"2017-04-28T06:22:20.285Z\", \"referenceNextUtc\": \"2017-04-28T06:29:43.667Z\", \"type\": \"feed\", \"berAverage\": 0.16100401059829558, \"transform\": \"none\" }]}")


def define_feed(feed_id=None):
    if not isinstance(feed_id, str):
        feed_id = str(feed_id)

    url = "http://fpsnext.vagrant.box:9000/v2/feeds/%s" % (feed_id)
    request_data = {"metadata": feed_id, "maxBacklog": 3600000}
    request_header = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(request_data), headers=request_header)
    print(response.status_code)
    print(response.request)
    print(response.text)


define_feed(feed_id=str(201604280602))


def send_request(ce_data=None):
    url = "http://fpsnext.vagrant.box:9000/v2/feeds/201604280601"
    out_put_file = "D:\\CecoComparision\\4.4(28-Apr-08Hr)\\base64\\Base641704280600_01.txt"

    with open(out_put_file, "r") as read_ce:
        ce_data = read_ce.read()

    if ce_data is not None:
        request_data = {'ceco': ce_data}

        response = requests.put(url=url, data=json.dumps(request_data), headers={'Content-Type': 'application/json'})

        print (response.status_code)
        print(response.headers)
        print(response.text)
    else:
        print("Empty Ce Data")


send_request()
