import requests
import json
import os

from operator import itemgetter


class FpsNext:
    def __init__(self):
        self.base_url = "http://192.168.217.175:9000/v2"

    def restart_search_workers(self):
        url = self.base_url + "/admin/clean"
        response = requests.post(url)

        return json.loads(response.text)

    def define_feed(self, feed_id=None, request_meta_data=None):
        if not isinstance(feed_id, str):
            feed_id = str(feed_id)

        url = self.base_url + "/feeds/%s" % (feed_id)
        if request_meta_data is None:
            request_meta_data = {"metadata": feed_id, "maxBacklog": 3600000}
        request_header = {'Content-Type': 'application/json'}

        response = requests.post(url, data=json.dumps(request_meta_data), headers=request_header)
        print("Define feed %s" % (str(response.status_code)))

        return response.status_code

    def ingest_feed(self, feed_id=None, ceco_data=None, ceco_file_path=None):
        url = self.base_url + "/feeds/" + feed_id

        if ceco_data is not None:
            request_data = {'ceco': ceco_data}

        else:
            if ceco_file_path is not None:
                with open(ceco_file_path, "r") as read_ce:
                    ceco_data = read_ce.read()
                request_data = {'ceco': ceco_data}
            else:
                print("cecoFilePath is Empty")

        response = requests.put(url=url, data=json.dumps(request_data), headers={'Content-Type': 'application/json'})
        print("Ingest_feed %s" % (str(response.status_code)))
        return response.status_code

    def identify_feed(self, ceco_data=None, analyze_ceco=True):
        url = self.base_url + "/identify?analyze=" + str(analyze_ceco)
        return_response = dict()
        if ceco_data is not None:
            request_data = {"ceco": "test", "maxResults": 500, "withSpeedTransform": True, "match": {"maxAge": 0}}
            request_data.update({"ceco": str(ceco_data)})

            response = requests.post(url=url, data=json.dumps(request_data),
                                     headers={'Content-Type': 'application/json'})
            print("Identify_feed %s" % (str(response.status_code)))
        return response.text

    def list_feeds(self):
        url = self.base_url + "/feeds"
        response = requests.get(url)
        return json.loads(response.text)

    def delete_feed(self, feed_id):
        url = self.base_url + "/feeds/" + str(feed_id)
        response = requests.delete(url)
        return response.status_code

    def ingest_cecos(self, ref_ceco_dir=None):
        for ref_ceco_file in os.listdir(ref_ceco_dir):
            print(ref_ceco_file)

    def read_fps_identify_results(json_string):
        json_obj = json.loads(json_string)
        sorted(json_obj.get('results'), key=itemgetter('candidateStartOffset'))

        print(json.dumps(json_obj))
        return json.dumps(json_obj)
