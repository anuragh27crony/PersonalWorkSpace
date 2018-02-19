import json
from datetime import datetime, timedelta

import os
import requests

from Ceco.Utils import Utils

min_base_url = "http://ec-vid-log-22.teletrax.com:8922/ldv/loq/3/"
ch_name = "Food_Network"
# channel_config_json = Utils(ch_name).channel_config
# hour_base_url = channel_config_json.get("Arbor").get("apiurl")
# arb_channel_index = channel_config_json.get("Arbor").get("channel_index")
timestamp = datetime.strptime("2017-12-14", '%Y-%m-%d')

# dest_dir = 'F:\\Dump\\CecoComparision\\4.4-4.5\\MSNBC\\03-Oct\\Arbor_Videos\\'
dest_dir = 'K:\\Scrap\\Anurag\\Arbor_Samples\\PAL\\ec-vid-log-22.teletrax.com_Antena3Romania'
dest_path = ""


def download_min_files(timestamp, start_offset=0):
    timestamp = timestamp + timedelta(minutes=start_offset)
    for minutes in range(start_offset, start_offset + 60):
        if minutes % 60 == 0:
            dest_path = os.path.join(dest_dir, timestamp.strftime("%y%m%d"), "{:02d}".format(timestamp.hour))
            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)
        else:
            dest_path = os.path.join(dest_dir, timestamp.strftime("%y%m%d"), "{:02d}".format(timestamp.hour))

        filename = timestamp.strftime("%y%m%d%H%M") + ".mp4"
        r = requests.get(min_base_url + filename)
        try:
            print(dest_path)
            with open(os.path.join(dest_path, filename), "wb") as write_file:
                write_file.write(r.content)
        except Exception as e:
            print("Error:" + filename)

        timestamp = timestamp + timedelta(minutes=1)


def return_hour_download_url(url, request_timeout_secs):
    resp = requests.get(url, timeout=request_timeout_secs)
    download_url_list = list()
    if resp.status_code == 200:
        response_json = json.loads(resp.text)
        if response_json.get("success"):
            response_data = response_json.get("data")
            for data_fragment in response_data.get("fragments"):
                download_url_list.append(data_fragment.get("location"))
        else:
            print("{0} --> response{1}".format(url, response_json))

    return download_url_list


def download_hour_files(channel_id, timestamp, request_timeout_secs=60):
    epoch_time = datetime(1970, 1, 1, 0, 0, 0)
    start_time = timestamp + timedelta(hours=8)
    end_time = start_time + timedelta(hours=1)

    base_url = "{0}/video?channelid={1}&".format(hour_base_url, channel_id)
    for hour in range(8, 24):
        start_epoch_secs = int((start_time - epoch_time).total_seconds())
        end_epoch_secs = int((end_time - epoch_time).total_seconds())
        # print("%s %s %s" % (hour, start_epoch_secs, end_epoch_secs))

        final_url = base_url + "start=" + str(start_epoch_secs) + "&stop=" + str(end_epoch_secs) + "&quality=full"
        try:
            fragment_urls = return_hour_download_url(final_url, request_timeout_secs)
            for url in fragment_urls:
                print(url)
        except Exception:
            print("Requesting again")
            fragment_urls = return_hour_download_url(final_url, request_timeout_secs)
            for url in fragment_urls:
                print(url)

        # timestamp = start_time + timedelta(hours=1)
        start_time = start_time + timedelta(hours=1)
        end_time = end_time + timedelta(hours=1)


# print("========== Channel Index :{0} ===============".format(arb_channel_index))
# download_hour_files(arb_channel_index, timestamp)
download_min_files(timestamp)
