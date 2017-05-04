import os
import platform

from subprocess import Popen, PIPE
from subprocess import CalledProcessError
from datetime import datetime, timedelta


def create_dirs(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    except OSError:
        print("Dir %s already exists" % (dir_path))


def run_cli(command_line):
    exit_code = -999
    try:
        print (command_line)
        p = Popen(command_line, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        output, err = p.communicate()
        rc = p.returncode
    except CalledProcessError as e:
        print(e)
    return rc


def build_ffmpeg_command(date_time=datetime.now(), out_file_path=os.getcwd(), target_fps=1, detector_id=None):
    font_file_path = "/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-R.ttf"
    fps = str(target_fps)

    if platform.system() == 'Windows':
        os.chdir('C://')
        font_file_path = "/Windows/Fonts/Arial.ttf"

    command_prefix = "ffmpeg -f lavfi -i testsrc=duration=60:size=320x240:rate=" + fps + " -vf \"drawtext=fontfile=" + font_file_path + ":timecode='"
    command_suffix = "':rate=" + fps + "::fontcolor=white:fontsize=40:x=w-tw-20:y=th+50:box=1:boxcolor=black@0.5:boxborderw=10,format=yuv420p\" -c:v libx264 -c:a copy -y"

    return ' '.join((command_prefix, date_time.strftime("%H\:%M\:%S\:00"), command_suffix, out_file_path))


def create_video_files_for_day(target_dir, date_time, channel_id, detector_id=None,video_fps=1):
    min_time_increment = timedelta(minutes=1)
    min_counter = 0

    date_str = "YYMMDD"
    channel = "ch"

    if not sample_videos:
        date_str = date_time.strftime("%y%m%d")
        channel = channel_id

    while min_counter < 1440:
        hour_folder_path = os.path.join(target_dir, date_str, date_time.strftime("%H"))
        create_dirs(hour_folder_path)
        output_file_name = "WcT%s%s%s_%s.mp4" % (detector_id, date_str, date_time.strftime("%H%M%S"), channel)
        return_code = run_cli(build_ffmpeg_command(date_time, os.path.join(hour_folder_path, output_file_name)))

        min_counter += 1
        date_time += min_time_increment



def generate_real_videos(detector_id, channel_list, no_of_days=1, date_str="2016-05-03"):
    # detector_id = os.getenv("DETECTOR_ID")
    # date = datetime.strptime(os.getenv("DATE"), '%Y-%m-%d')
    # no_of_days_back = int(os.getenv("DATES_BACK"))
    # channel_list = os.getenv("CHANNEL_LIST").split(",")


    # detector_id = "AAAA"

    for channel in channel_list:
        print("Starting Channel :" + '{0:02d}'.format(channel))
        channel_folder_path = os.path.join(os.getcwd(), detector_id, '{0:02d}'.format(channel))
        datetime_obj = datetime.strptime(date_str, '%Y-%m-%d')
        for day in range(no_of_days):
            create_video_files_for_day(target_dir=channel_folder_path, date_time=datetime_obj - timedelta(days=day),
                                       channel=channel)


def generate_sample_videos():
    video_fps = 1
    datetime_obj = datetime.strptime("2016-05-03", '%Y-%m-%d')
    create_video_files_for_day(date_time=datetime_obj, sample_videos=True, video_fps=video_fps)


generate_sample_videos()
generate_real_videos(detector_id="AAAA", channel_list=range(1, 2, 1), no_of_days=5,
                     date_str=datetime.now().strptime("%y%m%d"))

# find -name "*.mp4" -exec rename 's/None/AAAA/g' {} ";"
# Rename
