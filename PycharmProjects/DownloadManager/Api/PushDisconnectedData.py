import time
from datetime import datetime

import requests
import json


def fetch_and_push_data():
    detectors_set = set()
    dwld_mgr_url = "http://detector.teletrax.com/v1/prtg/channels"
    headers = {"Accept": "application/json"}
    time_stamp = datetime.utcnow().isoformat()
    try:
        response = requests.request("GET", dwld_mgr_url, headers=headers)
        if response.status_code is not 200:
            print(response.status_code)
        else:
            channel_data = json.loads(response.text)
            for channel in channel_data.get("configured"):
                detectors_set.add(channel.get("detectorName"))

            parse_detectors_data(detectors_set, time_stamp)
    except Exception as e:
        print(e)


def parse_detectors_data(detectors_set, time_stamp):
    for detector in detectors_set:
        insert_data = {"detectorId": detector, "timestamp": time_stamp}
        push_elastic_search(insert_data)


def push_elastic_search(data):
    elastic_url = "http://cvl-nj-log-001.teletrax.com:9200/detectors/disconnected"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.request("POST", elastic_url, headers=headers, data=json.dumps(data))
        if response.status_code is not 201:
            print(response.status_code)
    except Exception as e:
        print(e)


def initiate():
    push_frequency_in_secs = 60
    while True:
        start_time = time.time()
        fetch_and_push_data()
        exec_time_diff = time.time() - start_time
        if exec_time_diff < push_frequency_in_secs:
            time.sleep(push_frequency_in_secs - exec_time_diff)


if __name__ == '__main__':
    initiate()
