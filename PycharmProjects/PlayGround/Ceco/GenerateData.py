from random import randint, random
from datetime import datetime, timedelta
from decimal import *

import os


def generate_mux_filenames(startdatetime, enddatetime, seq):
    return "{2}_McV0130_{0}_{1}.mp4".format(startdatetime.strftime("%y%m%d%H%M"), enddatetime.strftime("%y%m%d%H%M"),
                                            seq)


def generate_trans_filenames(startdatetime, enddatetime, seq):
    return "{2}_TcV0130_{0}_{1}.mp4".format(startdatetime.strftime("%y%m%d%H%M"), enddatetime.strftime("%y%m%d%H%M"),
                                            seq)


def generate_vvcat(filepath_dir, startdatetime, enddatetime, ch_index, mux_filepath, trans_filepath):
    input_str = None
    getcontext().prec = 3
    input_duration = (enddatetime - startdatetime).total_seconds()
    total_files = int(input_duration // 60) + 2

    increment_datetime = startdatetime - timedelta(seconds=startdatetime.second)

    ce_datetime = startdatetime - timedelta(seconds=startdatetime.second, minutes=startdatetime.minute)

    nearest_15_min = 0 if startdatetime.minute < 15 else startdatetime.minute - (startdatetime.minute - 15)

    ce_datetime = startdatetime + timedelta(minutes=nearest_15_min)

    file_lst = list()

    ss_time = random() * 30
    duration_time = (enddatetime - startdatetime).total_seconds() - ss_time

    mux_cmd = ""
    trans_cmd = ""

    if os.path.isdir(filepath_dir):
        for file_increment in range(0, total_files):
            file_lst.append(
                os.path.join(filepath_dir, increment_datetime.strftime("%H"),
                             "WcV0130{0}_{1}.mp4".format(increment_datetime.strftime("%y%m%d%H%M%S"),
                                                         "{:02}".format(ch_index))))

            increment_datetime = increment_datetime + timedelta(minutes=1)

        input_str = ';'.join(file_lst)
        getcontext().prec = 3
        mux_cmd = "TtxVVCat.exe - i {0} -ss {1} -t {2} -c:v copy -o {3}".format(input_str, "{0:.3f}".format(ss_time),
                                                                                "{0:.3f}".format(duration_time),
                                                                                mux_filepath)
        getcontext().prec = 3
        trans_cmd = "TtxVVCat.exe - i {0} -ss {1} -t {2} -o {3}".format(input_str, "{0:.3f}".format(ss_time),
                                                                        "{0:.3f}".format(duration_time),
                                                                        trans_filepath)

    ce_file = "WcD0130{0}_{1}.ce".format(ce_datetime.strftime("%y%m%d%H%M"), "{:02}".format(ch_index))

    return mux_cmd, trans_cmd, ce_file


def random_generate(seq):
    rand_seconds = randint(1, 86400)
    rand_duration = randint(300, 400)
    startdatetime = datetime(2018, 2, 12, 0, 0, 0) + timedelta(seconds=rand_seconds)
    enddatetime = startdatetime + timedelta(seconds=rand_duration)

    input_files_dir = 'D:\\Dump\\CecoComparision\\4.5-4.4.17\\no_ts\\vids'
    mux_dir = 'D:\\Dump\\CecoComparision\\4.5-4.4.17\\no_ts\\5remux'
    trans_dir = 'D:\\Dump\\CecoComparision\\4.5-4.4.17\\no_ts\\5trans'

    mux_filepath = os.path.join(mux_dir, generate_mux_filenames(startdatetime, enddatetime, seq))
    trans_filepath = os.path.join(trans_dir, generate_trans_filenames(startdatetime, enddatetime, seq))

    (mux_cmd, trans_cmd, ce_file) = generate_vvcat(input_files_dir, startdatetime, enddatetime,
                                                   ch_index=3,
                                                   mux_filepath=mux_filepath,
                                                   trans_filepath=trans_filepath)

    return mux_cmd, trans_cmd, mux_filepath, trans_filepath, ce_file


mux_cmd_lst = list()
mux_files = list()
trans_cmd_lst = list()
trans_files = list()
ce_files = list()
for x in range(0, 100):
    (mux_cmd, trans_cmd, mux_filepath, trans_filepath, ce_file) = random_generate(x)
    mux_cmd_lst.append(mux_cmd)
    trans_cmd_lst.append(trans_cmd)

    mux_files.append(mux_filepath)
    trans_files.append(trans_filepath)
    ce_files.append(ce_file)

print(mux_cmd_lst)
print(trans_cmd_lst)
print(trans_files)
print(mux_files)
print(ce_files)
