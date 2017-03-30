import os
import uuid
import json
import datetime

from random import randint
from subprocess import check_output, CalledProcessError

output_dir = "D:\\civolution\\Data\\C31\\output3"
error_file_path = os.path.join(output_dir, "error.txt")
probe_file_path = os.path.join(output_dir, "probe.csv")
ffmpeg_cut_log_file = os.path.join(output_dir, "cutVideo.txt")


def write_file(file_path, data, mode='a+'):
    with open(file_path, mode) as file_write:
        file_write.write(data)


def ffmpeg_cut_transform(orig_file_path, output_file_path, start_secs=0, cut_file=True):
    if cut_file:
        start_time_string = "00:00:" + "{:0>2}".format(start_secs)
        duration_string = "00:00:" + "{:0>2}".format(60 - start_secs)

        # task = "ffmpeg -loglevel error -ss " + start_time_string + " -i " + input_file + "
        #
        #  -t " + duration_string + " " + out_file + " -y"
        task = "ffmpeg -loglevel error -ss " + start_time_string + " -i " + orig_file_path + " -c:v libx264 -bsf h264_mp4toannexb -t " + duration_string + " " + output_file_path + " -y"
    else:
        task = "ffmpeg -loglevel error -i " + orig_file_path + " -bsf h264_mp4toannexb " + output_file_path + " -y"

    try:
        output = check_output(task, shell=True).decode()
    except CalledProcessError:
        write_file(error_file_path, data=task)


def ffmpeg_concat(concat_file, out_file):
    task = "ffmpeg -loglevel error -f concat -safe 0 -i " + concat_file + " -absf aac_adtstoasc -movflags faststart -y " + out_file
    try:
        output = check_output(task, shell=True).decode()
    except CalledProcessError:
        write_file(error_file_path, data=task)


def ff_probe_details(input_file_path, output_file_path, expected_duration):
    task = "ffprobe -loglevel error -show_entries stream=bit_rate,avg_frame_rate,duration -print_format json -i " + input_file_path
    data = (expected_duration,)
    probe_data = ("bit_rate", "avg_frame_rate", "duration")

    try:
        output = check_output(task, shell=True).decode()
        stream_json = json.loads(output).get("streams")[0]

        for key in probe_data:
            data += (stream_json.get(key, ''),)
        final_data = ";".join(data)
        write_file(output_file_path, data=final_data + "\n")
    except CalledProcessError:
        write_file(error_file_path, data=task)


def random_detection_creator():
    margin_sec = 60
    detection_sec = randint(40, 950)

    detec_start_time = datetime.datetime(2017, 1, 28, randint(13, 20), randint(0, 59), randint(10, 59))
    start_time = detec_start_time + datetime.timedelta(seconds=margin_sec)

    detec_end_time = detec_start_time + + datetime.timedelta(seconds=detection_sec)
    end_time = detec_end_time + datetime.timedelta(seconds=margin_sec)
    return (start_time, end_time)


def create():
    datetime_strfmt = "%y%m%d%H%M%S"
    input_file_path = "D:\\\\civolution\\\\Data\\\\C31\\\\TotalVideos"

    for loop_iter in range(1):
        iter_out_path = os.path.join(output_dir, str(loop_iter))
        if not os.path.exists(iter_out_path):
            os.makedirs(iter_out_path)
        concat_file_name = os.path.join(iter_out_path, "concat.txt")

        mp4_ext = "_11.mp4"
        transport_stream_ext = "_11.ts"

        (start_time, end_time) = random_detection_creator()
        fragments = int((end_time - start_time).total_seconds() / 60)

        first_fragment = start_time - datetime.timedelta(seconds=start_time.second)
        in_file_name = os.path.join(input_file_path, "WcT0C31" + first_fragment.strftime(datetime_strfmt) + mp4_ext)
        uid = str(uuid.uuid4())

        out_file_name = os.path.join(input_file_path, "WcT0C31_" + uid + transport_stream_ext)
        write_file(file_path=ffmpeg_cut_log_file,
                   data="\t".join((str(loop_iter), start_time.isoformat(), out_file_name, "\n")))

        ffmpeg_cut_transform(in_file_name, out_file_name, start_time.second)
        ff_probe_details(out_file_name, output_file_path=probe_file_path, expected_duration=str(60 - start_time.second))

        write_file(concat_file_name, data="file " + str(input_file_path) + "\\\\WcT0C31_" + uid + transport_stream_ext + "\n")
        for fragment in range(1, fragments + 1):
            fragment_time = first_fragment + datetime.timedelta(minutes=fragment + 1)

            fragment_file_path = input_file_path + "\\\\WcT0C31_" + fragment_time.strftime(
                datetime_strfmt) + mp4_ext
            new_fragment_file_path = input_file_path + "\\\\WcT0C31_" + str(uuid.uuid4()) + transport_stream_ext
            write_file(concat_file_name, data="file " + new_fragment_file_path + "\n")

            ffmpeg_cut_transform(cut_file=False, orig_file_path=fragment_file_path,
                                 output_file_path=new_fragment_file_path)

        out_file_name = os.path.join(iter_out_path,
                                     start_time.strftime("%H%M%S") + "_" + end_time.strftime("%H%M%S") + ".mp4")
        ffmpeg_concat(concat_file_name, out_file_name)


create()
