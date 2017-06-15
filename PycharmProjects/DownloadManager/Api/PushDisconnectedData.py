import time
from datetime import datetime

import requests
import json

dwld_mgr_url = "http://detector.teletrax.com/v1/prtg"
accept_headers = {"Accept": "application/json"}


def fetch_connected_detectors():
    fetch_detectors = dwld_mgr_url + "/detectors"
    connected_detectors_list = list()
    try:
        response = requests.request("GET", fetch_detectors, headers=accept_headers)
        if response.status_code is not 200:
            print(response.status_code)
        else:
            channel_data = json.loads(response.text)
            for node_wise_detectors in channel_data:
                connected_detectors_list.extend(node_wise_detectors.get("detectors"))
    except Exception as e:
        print(e)
    return connected_detectors_list


def clean_disconnected_detectors(disconnected_detectors_set, connected_detectors_list):
    result_disconnected_detectors = disconnected_detectors_set.copy()
    for disconnected_detector in disconnected_detectors_set:
        if disconnected_detector in connected_detectors_list:
            result_disconnected_detectors.remove(disconnected_detector)
    print(result_disconnected_detectors)
    return result_disconnected_detectors


def fetch_disconnected_detectors():
    disconnected_detectors_set = set()
    fetch_channels = dwld_mgr_url + "/channels"

    try:
        response = requests.request("GET", fetch_channels, headers=accept_headers)
        if response.status_code is not 200:
            print(response.status_code)
        else:
            channel_data = json.loads(response.text)
            for channel in channel_data.get("configured"):
                disconnected_detectors_set.add(channel.get("detectorName"))


    except Exception as e:
        print(e)
    return disconnected_detectors_set


def parse_push_data_kibana(detectors_set, time_stamp):
    cleaned__disconnected_detectors_set = clean_disconnected_detectors(detectors_set, fetch_connected_detectors())
    for detector in cleaned__disconnected_detectors_set:
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

        time_stamp = datetime.utcnow().isoformat()
        disconnected_detectors_set = fetch_disconnected_detectors()
        parse_push_data_kibana(disconnected_detectors_set, time_stamp)

        exec_time_diff = time.time() - start_time
        if exec_time_diff < push_frequency_in_secs:
            time.sleep(push_frequency_in_secs - exec_time_diff)


if __name__ == '__main__':
    initiate()
