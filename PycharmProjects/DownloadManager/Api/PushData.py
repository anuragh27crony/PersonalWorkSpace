import time
from datetime import datetime

import requests
import json


def fetch_and_push_data():
    dwld_mgr_url = "http://detector.teletrax.com/v1/prtg/detectors"
    headers = {"Accept": "application/json"}
    time_stamp = datetime.utcnow().isoformat()
    try:
        response = requests.request("GET", dwld_mgr_url, headers=headers)
        if response.status_code is not 200:
            print(response.status_code)
        else:
            detector_data = json.loads(response.text)
            for region in detector_data:
                region_name = "us" in region.get("nodeName") and "us" or "rest"
                parse_detectors_data(region.get("detectors"), region_name, time_stamp)
    except Exception as e:
        print(e)


def parse_detectors_data(detectors_array, region, time_stamp):
    result = list()
    print("parsing")
    for detectorID in detectors_array:
        insert_data = {"detectorId": detectorID, "timestamp": time_stamp, "nodeName": region}
        push_elastic_search(insert_data)
    return result


def push_elastic_search(data):
    elastic_url = "http://cvl-nj-log-001.teletrax.com:9200/detectors/connected"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.request("POST", elastic_url, headers=headers, data=json.dumps(data))
        if response.status_code is not 200:
            print(response.status_code)
    except Exception as e:
        print(e)


def initiate():
    push_frequency_in_secs = 5
    while True:
        fetch_and_push_data()
        time.sleep(push_frequency_in_secs)


if __name__ == '__main__':
    initiate()
