import csv
import json
import os


class Utils:
    def __init__(self, channel_name):
        self.channel_config = self.read_channel_config(channel_name)

    def check_dir(self, dir_path):
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

    def read_channel_config(self, channel_name, config_file_path=None):

        if "cnews" in channel_name.lower():
            channel_name = "cnews"
        elif "tagg" in channel_name.lower():
            channel_name = "tagg"

        if not config_file_path:
            config_file_path = os.path.join(os.getcwd(), "ChannelDetails", channel_name + ".json")

        with open(config_file_path, "r") as config_file:
            channel_config = config_file.read()

        try:
            channel_config_json = json.loads(channel_config).get(channel_name)
        except Exception as e:
            print("Exception in reading channel config file")
            print(e)
            channel_config_json = {}
        return channel_config_json

    def list_files_dir(self, dir_path, file_ext=None):
        if file_ext:
            return [file for file in os.listdir(dir_path) if file.endswith(file_ext)]
        else:
            return [sub_dir for sub_dir in os.listdir(dir_path) if "." not in sub_dir]

    def write_results(self, path, data, detec_version=None, format=None):
        if format:
            file_name = os.path.join(path, detec_version) + ".json"
            with open(file_name, 'a+') as txt_file:
                txt_file.write(data)
        else:
            file_name = os.path.join(path, detec_version) + ".csv"
            with open(file_name, 'a+') as csv_file:
                cw = csv.writer(csv_file)
                cw.writerow(list(data))
