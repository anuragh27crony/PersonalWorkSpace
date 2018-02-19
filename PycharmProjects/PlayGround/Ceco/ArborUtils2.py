import json

import requests
from datetime import timedelta, datetime

from Ceco.Utils import Utils


class ArborUtils(Utils):
    def __init__(self, channel_name):
        super().__init__(channel_name)
        self.h_file_datetime_pattern = "%y%m%d%H"

        arb_ch_details = self.channel_config.get("Arbor")

        self.channel_index = arb_ch_details.get("channel_index")
        self.api_url = arb_ch_details.get("apiurl")

    def create_arbor_hour_file(self, datetime, channel_index):
        file_name = "{0}_{1}.mp4".format(channel_index, datetime.strftime(self.h_file_datetime_pattern))
        return file_name

    @staticmethod
    def return_hour_download_url(url, request_timeout_secs):
        download_url_list = list()
        try:
            resp = requests.get(url, timeout=request_timeout_secs)
            if resp.status_code == 200:
                response_json = json.loads(resp.text)
                if response_json.get("success"):
                    response_data = response_json.get("data")
                    for data_fragment in response_data.get("fragments"):
                        download_url_list.append(data_fragment.get("location"))
                else:
                    print("{0} --> response{1}".format(url, response_json))
        except Exception:
            print("error")
        return download_url_list

    def download_hour_files(self, timestamp, request_timeout_secs=60, start_hour=0, end_hour=24):
        epoch_time = datetime(1970, 1, 1, 0, 0, 0)

        base_url = "{0}/video?channelid={1}&".format(self.api_url, self.channel_index)
        for hour in range(start_hour, end_hour):
            start_time = timestamp + timedelta(hours=hour)
            end_time = timestamp + timedelta(hours=hour + 1)
            start_epoch_secs = int((start_time - epoch_time).total_seconds())
            end_epoch_secs = int((end_time - epoch_time).total_seconds())

            final_url = base_url + "start=" + str(start_epoch_secs) + "&stop=" + str(end_epoch_secs) + "&quality=full"
            print(final_url)
            # try:
            #     fragment_urls = self.return_hour_download_url(final_url, request_timeout_secs)
            #     for url in fragment_urls:
            #         print(url)
            # except Exception:
            #     print("Requesting again")
            #     fragment_urls = self.return_hour_download_url(final_url, request_timeout_secs)
            #     for url in fragment_urls:
            #         print(url)
                    # finally:


# ch_list = ["5kanal", "lrt", "rai1", "rai3", "tvn24", "tv5monde", "rtsun", "srf1", "net5"]

# rte2

ch_list = ["tagg"]

for ch_name in ch_list:
    channel_config_json = Utils(ch_name).channel_config
    ch_arbor_util = ArborUtils(ch_name)
    timestamp = datetime.strptime("2017-11-28", '%Y-%m-%d')
    print("========== Channel  :{0} ===============".format(ch_name))
    start_hour = 9
    end_hour = 24
    ch_arbor_util.download_hour_files(timestamp, start_hour=start_hour, end_hour=end_hour)

    timestamp = datetime.strptime("2017-11-29", '%Y-%m-%d')
    print("========== Channel  :{0} ===============".format(ch_name))
    start_hour = 0
    end_hour = 6
    ch_arbor_util.download_hour_files(timestamp, start_hour=start_hour, end_hour=end_hour)