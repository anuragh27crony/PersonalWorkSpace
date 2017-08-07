#!/bin/python
import os
from datetime import datetime, timedelta

def create_dir(dir_path):
    try:
        if not os.path.exists(dir_path):
                os.mkdir(dir_path)
    except OSError:
        print("Dir %s already exists" % (dir_path))

detector_id = os.getenv("DETECTOR_ID")
date = datetime.strptime(os.getenv("DATE"), '%Y-%m-%d')
no_of_days_back = int(os.getenv("DATES_BACK"))
channel_list = os.getenv("CHANNEL_LIST").split(",")
files = os.listdir("./data/DataTemplate")
pattern = "WcT%s%s%s%s00_%s.mp4"

for channel in channel_list:
    # Create Channel Folder
    channel_folder_path = "./%s/%s" % (detector_id, channel)
    create_dir(channel_folder_path)
    # os.mkdir(channel_folder_path)
    for day in range(no_of_days_back):
        current_day=date-timedelta(days=day)
        # Create date folder
        day_folder_path = os.path.join(channel_folder_path, current_day.strftime("%y%m%d"))
        # if not os.path.exists(day_folder_path):
        #     os.mkdir(day_folder_path)
        create_dir(day_folder_path)
        for hour in range(24):
            current_day_hour = current_day + timedelta(hours=hour)
            #Create Hour folder
            hour_folder_path = os.path.join(day_folder_path , current_day_hour.strftime("%H"))
            # if not os.path.exists(hour_folder_path):
            #     os.mkdir(hour_folder_path)
            create_dir(hour_folder_path)
            for minute in range(60):
                current_day_hour_min = current_day_hour + timedelta(minutes=minute)
                filename = pattern % (detector_id,
                                    current_day_hour_min.strftime("%y%m%d"),
                                    current_day_hour_min.strftime("%H"),
                                    current_day_hour_min.strftime("%M"),
                                    channel)
                #print(folder_path_temp + "/" + filename)
                try:
                    os.symlink( os.getcwd()+ "/data/DataTemplate/%s.mp4" % str(minute), hour_folder_path + "/" + filename)
                except Exception as e:
                    print(e)
                    print("ERROR:",folder_path_temp + "/" + filename)
                    #import pdb;pdb.set_trace()