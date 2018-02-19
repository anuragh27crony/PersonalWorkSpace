import os
from subprocess import Popen, PIPE

from subprocess import CalledProcessError
from datetime import datetime, timedelta

import time


def run_cli(command_line):
    exit_code = -999
    try:
        # cmd_output = subprocess.check_output(command_line, shell=True)
        p = Popen(command_line, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
        output, err = p.communicate()
        rc = p.returncode
    except CalledProcessError as e:
        print(e)
    return rc


def create_cli(time_ticker, output_dir, channel_id_str):
    os.chdir('C://')
    command_prefix = "ffmpeg -f lavfi -i testsrc=duration=60:size=320x240:rate=1 -vf \"drawtext=fontfile=/Windows/Fonts/Arial.ttf:timecode='"
    command_suffix = "':rate=29.97::fontcolor=white:fontsize=40:x=w-tw-20:y=th+50:box=1:boxcolor=black@0.5:boxborderw=10,format=yuv420p\" -c:v libx264 -c:a copy -y "
    output_file_path = create_output_filename(time_ticker, output_dir, channel_id_str)
    return ' '.join((command_prefix, time_ticker.strftime("%H\:%M\:%S\:00"), command_suffix, output_file_path))


def create_output_filename(time_ticker, output_dir, channel_id_str):
    detector_id = "0001"
    pattern = "WcT%s%s00_%s.mp4"
    file_name = pattern % (detector_id, time_ticker.strftime("%y%m%d%H%M%S"), channel_id_str)
    # file_name = "WcT" + detector_id + time_ticker.strftime("%y%m%d%H%M%S") + "_" + channel_id_str + ".mp4"
    return os.path.join(output_dir, file_name)


def wait_process(rc):
    wait_increment = 1
    if rc > -1:
        time.sleep(wait_increment)


def create_min_files():
    min_time_increment = timedelta(minutes=1)
    time_ticker = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    min_counter = 0
    channel_id = 1
    channel_id_str = '{:02d}'.format(channel_id)

    while min_counter < 1440:
        output_dir = os.path.join("D:", os.sep, channel_id_str, time_ticker.strftime("%y%m%d"),
                                  time_ticker.strftime("%H"))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        rc = run_cli(create_cli(time_ticker, output_dir, channel_id_str))

        min_counter += 1
        time_ticker += min_time_increment
