#!/bin/python
import os
from datetime import datetime, timedelta

def create_dirs(dir_path):
    try:
        if not os.path.exists(dir_path):
                os.mkdirs(dir_path)
    except OSError:
        print("Dir %s already exists" % (dir_path))


def create_video_files_for_day(target_dir,date_time,channel_id):
    output_file_name = "WcT%s%s00_%s.mp4" % (detector_id, time_ticker.strftime("%y%m%d%H%M%S"), channel_id)
    min_time_increment = timedelta(minutes=1)
        while min_counter < 1440:
            hour_folder_path=os.path.join(target_dir,date_time.strftime("%y%m%d"), date_time.strftime("%H"))
            create_dirs(hour_folder_path)

            #Run the FFMpeg Command

            min_counter+=1
            current_day+=min_time_increment

detector_id = os.getenv("DETECTOR_ID")
date = datetime.strptime(os.getenv("DATE"), '%Y-%m-%d')
no_of_days_back = int(os.getenv("DATES_BACK"))
channel_list = os.getenv("CHANNEL_LIST").split(",")



for channel in channel_list:
    # Create Channel Folder
    channel_folder_path = "./%s/%s" % (detector_id, channel)

    for day in range(no_of_days_back):
        create_video_files_for_day(channel_folder_path,date-timedelta(days=day))
