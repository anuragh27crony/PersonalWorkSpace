import os
from subprocess import run, call, PIPE

import time

from Ceco.Base64CecoFile import AnalyzeCeco

channel_name = "UDP"
date_str = "17-Oct"

detec_channel_index = "03"
arb_channel_index = "8"

is_arbor = False

base_dir_path = os.path.join("F:\\Dump\\CecoComparision", channel_name, date_str)

arb_vids_path = "Arbor_Videos"
# dete_vids_path = "4.5_Videos"
dete_vids_path = "QSD-2000"

dete_vid_file_prefix = "WtV0C23171017"
arb_vid_file_prefix = "WtQ0A00171003"

dete_hour_vid_file_prefix = "A_HourLong"
arb_hour_vid_file_prefix = "{0}_20171015".format(arb_channel_index)

dete_ref_ceco_file_prefix = "ref_45_hour_"
arb_ref_ceco_file_prefix = "ref_Arbor_hour_"

arb_ref_version = "Ref_Arbor"
detec_ref_version = "Ref_4.5"

arb_min_file_suffix = ".mp4"
detec_min_file_suffix = "00_{0}.mp4".format(detec_channel_index)

arb_hour_file_suffix = ".mp4"
detec_hour_file_suffix = "00.mp4"

detec_results_file_prefix = "Day_Analysis_Detec_"
arb_results_file_prefix = "Day_Analysis_Arb_"

if is_arbor:
    min_vid_dir_path = os.path.join(base_dir_path, arb_vids_path)
    min_video_file_prefix = arb_vid_file_prefix
    hour_vid_file_prefix = arb_hour_vid_file_prefix
    ref_ceco_file_prefix = arb_ref_ceco_file_prefix
    ref_ver = arb_ref_version
    min_file_suffix = arb_min_file_suffix
    hour_file_suffix = arb_hour_file_suffix
    results_file_name = arb_results_file_prefix + channel_name + "_" + date_str
else:
    min_vid_dir_path = os.path.join(base_dir_path, dete_vids_path)
    min_video_file_prefix = dete_vid_file_prefix
    hour_vid_file_prefix = dete_hour_vid_file_prefix
    ref_ceco_file_prefix = dete_ref_ceco_file_prefix
    ref_ver = detec_ref_version
    min_file_suffix = detec_min_file_suffix
    hour_file_suffix = detec_hour_file_suffix
    results_file_name = detec_results_file_prefix + channel_name + "_" + date_str


def check_dir(dir_path):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)


def create_min_ts_files_concat_txt(hour_str):
    hour_dir_path = os.path.join(min_vid_dir_path, hour_str)
    command_prefix = 'ffmpeg.exe -hide_banner  -loglevel error -i '
    # ffmpeg_args = ' -filter:v "crop=in_w:in_h-12:0:0" -b:v 2000k -c:a copy -y ' #Just Cropping burned Timestamps
    # video_ffmpeg_args = ' -filter:v "crop=in_w:in_h-12:0:0" -b:v 2500k -an -movflags faststart -y '  #
    video_ffmpeg_args = ' -an -c:v copy -y '  #
    audio_ffmpeg_args = ' -filter:v "crop=in_w:in_h-12:0:0" -b:v 2000k -an -y '  #

    concat_file_list_path = os.path.join(hour_dir_path, "concat_audioless.txt")
    cropped_vids_dir = os.path.join(hour_dir_path, "audioless")
    check_dir(cropped_vids_dir)

    for minute in range(60):
        min_str = "{:02d}".format(minute)
        min_mp4_file_name = min_video_file_prefix + hour_str + min_str + min_file_suffix
        input_file_path = os.path.join(hour_dir_path, min_mp4_file_name)
        crop_file_path = os.path.join(cropped_vids_dir, min_mp4_file_name)
        final_cmd = command_prefix + input_file_path + video_ffmpeg_args + crop_file_path
        # print(final_cmd)
        call(final_cmd, shell=True)
        # output = run(final_cmd, stdout=PIPE, check=True)

        with open(concat_file_list_path, "a+") as file:
            file.writelines("file '" + crop_file_path + "'")
            file.writelines("\n")

    return concat_file_list_path


def concat_ts_files(concat_file_list_path, output_file_path):
    # cmd_prefix = "ffmpeg.exe  -hide_banner -loglevel error "
    # cmd_prefix_2 = "-f concat -safe 0 -i "
    # ffmpeg_args = " -c copy -bsf:a aac_adtstoasc -movflags faststart -y "

    cmd_prefix = "ffmpeg.exe  -hide_banner -loglevel error "
    cmd_prefix_2 = "-f concat -safe 0 -i "
    # ffmpeg_args = " -c copy -y "  # WithAudio
    ffmpeg_args = ' -filter:v "crop=in_w:in_h-12:0:0" -bsf:a aac_adtstoasc  -b:v 2500k -movflags faststart -y '

    final_cmd = cmd_prefix + cmd_prefix_2 + concat_file_list_path + ffmpeg_args + output_file_path
    print(final_cmd)
    try:
        call(final_cmd, shell=True)
        # output = run(final_cmd, stdout=PIPE, check=True)
    except Exception as e:
        print(e)


def create_ref_ceco(media_file_name, ref_ceco_dir, ref_ceco_name):
    ceco_gen_cmd_prefix = 'python E:\\GitRepos\\PersonalWorkSpace\\PycharmProjects\\PlayGround\Ceco\\FPToolGenerateCECO.py --media '
    ceco_gen_args = ' --algorithms VIDEO_ALGO_V5_4_65S --ceco '
    ref_ceco_path = os.path.join(ref_ceco_dir, ref_ceco_name)

    try:
        final_cmd = ceco_gen_cmd_prefix + media_file_name + ceco_gen_args + ref_ceco_path
        call(final_cmd, shell=True)
    except Exception as e:
        print(e)


def create_hour_ref_cecos(hour_str, ref_ceco_dir):
    final_mp4_concat_file = hour_vid_file_prefix + hour_str + hour_file_suffix

    if not is_arbor:
        hour_mp4_file_path = os.path.join(min_vid_dir_path, hour_str, final_mp4_concat_file)
        if not os.path.isfile(hour_mp4_file_path):
            concat_file_list_path = create_min_ts_files_concat_txt(hour_str)
            concat_ts_files(concat_file_list_path, hour_mp4_file_path)
    else:
        hour_mp4_file_path = os.path.join(min_vid_dir_path, final_mp4_concat_file)

    ref_ceco_name = ref_ceco_file_prefix + hour_str + ".ceco"
    if not os.path.isfile(os.path.join(ref_ceco_dir, ref_ceco_name)):
        create_ref_ceco(hour_mp4_file_path, ref_ceco_dir, ref_ceco_name)

    return os.path.join(ref_ceco_dir, ref_ceco_name)


def create_min_ref_cecos(hour_str, ref_ceco_dir):
    print("Creating Min Ref for Hour" + hour_str)
    ref_ceco_name_list = list()
    for minute in range(60):
        min_str = "{:02d}".format(minute)

        min_mp4_file_name = min_video_file_prefix + hour_str + min_str + min_file_suffix
        min_mp4_file_path = os.path.join(min_vid_dir_path, hour_str, min_mp4_file_name)

        ref_ceco_name = ref_ceco_file_prefix + hour_str + min_str + ".ceco"
        create_ref_ceco(min_mp4_file_path, ref_ceco_dir, ref_ceco_name)
        ref_ceco_name_list.append(ref_ceco_name)

    return ref_ceco_name_list


def analyze_candidate_cecos(candidate_ceco_dir, ceco_filename_list, candidate_ver="0.0", ref_ver="Ref_0.0",
                            results_file_name="test_results"):
    for candidate_ceco_file_name in ceco_filename_list:
        result_list = [ref_ver, candidate_ver, candidate_ceco_file_name]
        (missing_ce, avg_ber_value, result) = analyze_ceco.analyze_candidate_ceco(candidate_ceco_dir,
                                                                                  candidate_ceco_file_name)
        result_list.append(len(missing_ce))
        result_list.append(avg_ber_value)
        result_list.append(missing_ce)
        # result_list.append(result)
        analyze_ceco.write_results(results_dir, tuple(result_list), results_file_name)


def create_ceco_file_hour_list(file_prefix, detec_mac, date_str, hour_str, file_suffix):
    ceco_file_list = list()
    for interval in range(0, 60, 15):
        min_interval_str = "{:02d}".format(interval)
        ceco_file_list.append(file_prefix + detec_mac + date_str + hour_str + min_interval_str + file_suffix)
    return ceco_file_list


ref_ceco_base_dir = os.path.join(base_dir_path, "Ref_Cecos_2000")

analyze_ceco = AnalyzeCeco()
results_dir = os.getcwd()

for hour in range(9, 24):
    if hour != 100:
        hour_str = "{:02d}".format(hour)

        ref_ceco_dir = os.path.join(ref_ceco_base_dir, hour_str)
        check_dir(ref_ceco_dir)

        ref_ceco_name_list = list()
        ref_ceco_name_list.append(create_hour_ref_cecos(hour_str, ref_ceco_dir))

        ingest_result = False
        for ref_ceco in ref_ceco_name_list:
            analyze_ceco.clean_existing_feeds()
            ingest_result = analyze_ceco.ingest_ref_ceco(ref_ceco_dir, ref_ceco, hour_str + "0000")

        if ingest_result:
            ceco_prefix_44 = "WcD0D21171017"
            ceco_suffix_44 = "_01.ce"
            ceco_prefix_45 = "WcD0C23171017"
            ceco_suffix_45 = "_01.ce".format(detec_channel_index)

            candidate_ver = "C4.4"
            candidate_ceco_dir = os.path.join(base_dir_path, "4.4_ceco", "collection")
            candidate_ceco_file_list = [ceco_prefix_44 + hour_str + "00" + ceco_suffix_44,
                                        ceco_prefix_44 + hour_str + "15" + ceco_suffix_44,
                                        ceco_prefix_44 + hour_str + "30" + ceco_suffix_44,
                                        ceco_prefix_44 + hour_str + "45" + ceco_suffix_44]

            analyze_candidate_cecos(candidate_ceco_dir, candidate_ceco_file_list, candidate_ver, ref_ver,
                                    results_file_name)

            candidate_ver = "C4.5"
            candidate_ceco_dir = os.path.join(base_dir_path, "4.5_ceco", "collection")
            candidate_ceco_file_list = [ceco_prefix_45 + hour_str + "00" + ceco_suffix_45,
                                        ceco_prefix_45 + hour_str + "15" + ceco_suffix_45,
                                        ceco_prefix_45 + hour_str + "30" + ceco_suffix_45,
                                        ceco_prefix_45 + hour_str + "45" + ceco_suffix_45, ]
            analyze_candidate_cecos(candidate_ceco_dir, candidate_ceco_file_list, candidate_ver, ref_ver,
                                    results_file_name)

            analyze_ceco.fpsnext.restart_search_workers()
            time.sleep(10)
