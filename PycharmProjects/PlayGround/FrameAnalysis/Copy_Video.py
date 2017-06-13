#!/bin/python
import os
import shutil

from subprocess import Popen, PIPE
from subprocess import CalledProcessError
from datetime import datetime, timedelta

def run_cli(command_line):
    exit_code = -999
    try:
        print (command_line)
        p = Popen(command_line, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
        output, err = p.communicate()
        rc = p.returncode
        print("Output is %s" % output)
        print("Return Code is %s" % rc)
    except CalledProcessError as e:
        print(e)
    return rc

def copy_verification_videos(video_src_dir):
    detector_id = os.getenv("DETECTOR_ID")
    date = datetime.strptime(os.getenv("DATE"), '%Y-%m-%d')
    no_of_days_back = int(os.getenv("DATES_BACK"))
    channel_list = os.getenv("CHANNEL_LIST").split(",")

    for channel in channel_list:
        detector_folder_path=os.path.join(".","data",detector_id)
        channel_folder_path=os.path.join(detector_folder_path, channel)

        for day in range(no_of_days_back):
            current_day=date-timedelta(days=day)
            date_str=current_day.strftime("%y%m%d")

            # Copy the Hourly Folder from the unzipped Data Template.
            try:
                day_folder_path = os.path.join(channel_folder_path, date_str)
                if not os.path.exists(day_folder_path):
                    shutil.copytree(src=video_src_dir,dst=day_folder_path)
                datetime_regex="'s/YYMMDD/"+date_str+"/g'"
                bash_command="find -path '%s*.mp4' -exec rename -v %s {} ';'" % (os.path.abspath(day_folder_path),datetime_regex)
                run_cli(bash_command)

            except Exception as e:
                print("Printing Error")
                print(e)
        try:
            channel_regex="'s/ch/"+channel+"/g'"
            bash_command="find -path '%s*.mp4' -exec rename -v %s {} ';'" % (os.path.abspath(channel_folder_path),channel_regex)
            run_cli(bash_command)

            detector_regex="'s/None/"+str(detector_id)+"/g'"
            bash_command="find -path '%s*.mp4' -exec rename -v %s {} ';'" % (os.path.abspath(detector_folder_path),detector_regex)
            run_cli(bash_command)
        except Exception as e:
            print(e)

import sys
print(sys.argv[1])
if sys.argv[1] is not None:
    copy_verification_videos(video_src_dir=str(sys.argv[1]))
else:
    print("Missing Target Dir path")