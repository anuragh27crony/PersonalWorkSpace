import os

from subprocess import call

import shutil
import time

from datetime import timedelta, datetime

from Ceco import FpsUtil
from Ceco.Utils import Utils


class DetectorUtils(Utils):
    def __init__(self, channel_name):
        super().__init__(channel_name)

        self.FpsUtil = FpsUtil.FpsUtil()

        self.detec_ceco_file_datetime_pattern = "%y%m%d%H%M"
        self.detec_media_file_datetime_pattern = "%y%m%d%H%M%S"

        self.sanitized_min_files_dir = "audioless"
        self.concat_min_file_filename = "concat_audioless.txt"

        self.media_ext = ".mp4"
        self.ceco_ext = ".ce"
        self.results_dir = os.getcwd()

        detec_channel_details = self.channel_config.get("DetectorLogging")
        candi_channel_details = dict()
        for candidate in self.channel_config.get("candidate"):
            candi_ver = str(candidate.pop("version"))
            candi_channel_details.update({candi_ver: candidate})

        self.min_vid_base_dir = detec_channel_details.get("dirpath")
        self.is_qsd = detec_channel_details.get("isqsd")

        self._45_ch_index = "{:02d}".format(detec_channel_details.get("channel_index"))
        self._45_mac_id = candi_channel_details.get("4.5").get("mac")
        self._44_mac_id = candi_channel_details.get("4.4").get("mac")
        self._44_ch_index = "{:02d}".format(candi_channel_details.get("4.4").get("channel_index"))

    def create_detec_filename(self, datetime, is_ceco=False, timestamp_bruned=True, mac_id=None, ch_index=None):
        filename = list()
        if is_ceco:
            filename.append("WcD")
            time_formatter = self.detec_ceco_file_datetime_pattern
            file_ext = self.ceco_ext
        else:
            filename.append("Wt") if timestamp_bruned else filename.append("Wv")
            filename.append("Q") if self.is_qsd else filename.append("V")
            time_formatter = self.detec_media_file_datetime_pattern
            file_ext = self.media_ext

        mac_addr = self._45_mac_id if not mac_id else mac_id
        ch_index = self._45_ch_index if not ch_index else ch_index

        filename.append(
            "{0}{1}_{2}{3}".format(str(mac_addr).upper(), datetime.strftime(time_formatter), ch_index, file_ext))
        return ''.join(filename)

    def candidate_ce_lst(self, date=None, hour_str=None, is_45=False):
        ce_file_lst = list()

        if not isinstance(hour_str, int):
            hour_str = int(hour_str)

        mac_addr = ch_index = None
        if not is_45:
            mac_addr = self._44_mac_id
            ch_index = self._44_ch_index

        for interval in range(4):
            datetime = date + timedelta(hours=hour_str, minutes=15 * interval)
            ce_file_lst.append(self.create_detec_filename(datetime, is_ceco=True, mac_id=mac_addr, ch_index=ch_index))

        return ce_file_lst

    def arb_hour_file(self, date=None, hour_str=None):
        ch_index = self.channel_config.get("Arbor").get("channel_index")
        return "{0}_{1}{2}.mp4".format(ch_index, date.strftime("%Y%m%d"), hour_str)

    def stitch_min_files(self, concat_file_list_path, output_file_path):
        cmd_prefix = "ffmpeg.exe  -hide_banner -loglevel error "
        cmd_prefix_2 = "-f concat -safe 0 -i "
        ffmpeg_args = ' -filter:v "crop=in_w:in_h-12:0:0" -bsf:a aac_adtstoasc  -b:v 2500k -movflags faststart -y '

        final_cmd = cmd_prefix + cmd_prefix_2 + concat_file_list_path + ffmpeg_args + output_file_path
        try:
            call(final_cmd, shell=True)
        except Exception as e:
            print("Inside Stitch Min Files Module")
            print(e)

    def sanitize_min_files(self, ch_hour_dir_path):
        command_prefix = 'ffmpeg.exe -hide_banner  -loglevel error -i '
        video_ffmpeg_args = ' -an -c:v copy -y '  #

        concat_txt_file = os.path.join(ch_hour_dir_path, self.concat_min_file_filename)
        sanitized_min_files_dir = os.path.join(ch_hour_dir_path, self.sanitized_min_files_dir)
        self.check_dir(sanitized_min_files_dir)

        min_mp4_files_list = self.list_files_dir(ch_hour_dir_path, ".mp4")

        for min_mp4_file in min_mp4_files_list:
            input_file_path = os.path.join(ch_hour_dir_path, min_mp4_file)
            sanitized_mp4_file = os.path.join(sanitized_min_files_dir, min_mp4_file)
            final_cmd = command_prefix + input_file_path + video_ffmpeg_args + sanitized_mp4_file

            call(final_cmd, shell=True)

            with open(concat_txt_file, "a+") as file:
                file.writelines("file '" + sanitized_mp4_file + "'\n")

        return concat_txt_file

    def create_ref_ceco(self, media_file_name, ref_ceco_file_path):
        ceco_gen_cmd_prefix = 'python E:\\GitRepos\\PersonalWorkSpace\\PycharmProjects\\PlayGround\Ceco\\FPToolGenerateCECO.py --media '
        ceco_gen_args = ' --algorithms VIDEO_ALGO_V5_4_65S --ceco '

        try:
            final_cmd = ceco_gen_cmd_prefix + media_file_name + ceco_gen_args + ref_ceco_file_path
            call(final_cmd, shell=True)
        except Exception as e:
            print(e)

    def analyze_candidate_cecos(self, candidate_ceco_dir, ceco_filename_list, candidate_ver="0.0", ref_ver="Ref_0.0",
                                results_file_name="test_results"):

        for candidate_ceco_file_name in ceco_filename_list:
            result_list = [ref_ver, candidate_ver, candidate_ceco_file_name]
            (missing_ce, avg_ber_value, result) = self.FpsUtil.analyze_candidate_ceco(candidate_ceco_dir,
                                                                                      candidate_ceco_file_name)
            if not missing_ce:
                missing_ce = set()
            result_list.append(len(missing_ce))
            result_list.append(avg_ber_value)
            result_list.append(missing_ce)
            # result_list.append(result)
            self.write_results(self.results_dir, tuple(result_list), results_file_name)


ch_list = ["msnbc", "foxnews"]

for ch_name in ch_list:
    print(ch_name)
    detec_ch_util = DetectorUtils(ch_name.lower())

    base_dir = os.path.join("F:\\Dump\\CecoComparision\\NTSC", ch_name, "26-nov")
    vids_dir = os.path.join(base_dir, "4.5_videos")
    arb_vids_dir = os.path.join(base_dir, "Arbor_Videos")
    ref_ceco_dir = os.path.join(base_dir, "Ref_Cecos")
    arb_ref_ceco_dir = os.path.join(base_dir, "Ref_Cecos", "arb")

    detec_ch_util.check_dir(ref_ceco_dir)
    detec_ch_util.check_dir(arb_ref_ceco_dir)

    ce_hourfile_prefix = "arb_HourLong"
    # arb_hour_files = detec_ch_util.list_files_dir(arb_vids_dir, "mp4")
    # print(arb_hour_files)
    # for arb_hour_file in arb_hour_files:
    #     hour_dir = arb_hour_file[-6:-4]
    #     print(hour_dir)
    #     hour_mp4_file = os.path.join(arb_vids_dir, arb_hour_file)
    #     hour_ref_ceco_file = os.path.join(arb_ref_ceco_dir, ce_hourfile_prefix + hour_dir + ".ce")
    #
    #     if not os.path.isfile(hour_ref_ceco_file):
    #         detec_ch_util.create_ref_ceco(hour_mp4_file, hour_ref_ceco_file)

            # hourfile_prefix = "HourLong"
            # hour_dirs_list = detec_ch_util.list_files_dir(vids_dir)
            # for hour_dir in hour_dirs_list:
            #     hour_dir_path = os.path.join(vids_dir, hour_dir)
            #     hour_mp4_file = os.path.join(vids_dir, hourfile_prefix + hour_dir + ".mp4")
            #     hour_ref_ceco_file = os.path.join(ref_ceco_dir, hourfile_prefix + hour_dir + ".ce")
            #
            #     if not os.path.isfile(hour_ref_ceco_file):
            #         if not os.path.isfile(hour_mp4_file):
            #             concat_txt_file = detec_ch_util.sanitize_min_files(hour_dir_path)
            #             detec_ch_util.stitch_min_files(concat_txt_file, hour_mp4_file)
            #         tmp_vids_dir = os.path.join(hour_dir_path, "audioless")
            #         try:
            #             shutil.rmtree(tmp_vids_dir)
            #         except Exception:
            #             print("Error in removing path")
            #         detec_ch_util.create_ref_ceco(hour_mp4_file, hour_ref_ceco_file)

    ingest_result = True
    ref = "ref_4.5"

    if "cnews_f_1600" in ch_name.lower():
        ref_ceco_dir_lst = [arb_ref_ceco_dir]
    else:
        ref_ceco_dir_lst = [ref_ceco_dir, arb_ref_ceco_dir]

    for ceco_dir in ref_ceco_dir_lst:
        if "arb" in ceco_dir:
            ch_name = "arb_" + ch_name
            ref = "ref_Arbor"
        for ref_ceco in detec_ch_util.list_files_dir(ceco_dir, "ce"):
            hour_dir = ref_ceco[-5:-3]
            date_obj = datetime.strptime("171126", '%y%m%d')

            detec_ch_util.FpsUtil.clean_existing_feeds()
            ingest_result = detec_ch_util.FpsUtil.ingest_ref_ceco(ceco_dir, ref_ceco, hour_dir + "0000")

            if ingest_result:
                candidate_ver = "C4.4"
                candidate_ceco_dir = os.path.join(base_dir, "4.4_ceco", "collection")

                candidate_ceco_file_list = detec_ch_util.candidate_ce_lst(date=date_obj, hour_str=hour_dir,
                                                                          is_45=False)
                detec_ch_util.analyze_candidate_cecos(candidate_ceco_dir, candidate_ceco_file_list,
                                                      candidate_ver,
                                                      ref,
                                                      ch_name)

                candidate_ver = "C4.5"
                candidate_ceco_dir = os.path.join(base_dir, "4.5_ceco", "collection")
                candidate_ceco_file_list = detec_ch_util.candidate_ce_lst(date=date_obj, hour_str=hour_dir,
                                                                          is_45=True)
                detec_ch_util.analyze_candidate_cecos(candidate_ceco_dir, candidate_ceco_file_list,
                                                      candidate_ver,
                                                      ref,
                                                      ch_name)

                detec_ch_util.FpsUtil.restart_search_workers()
                time.sleep(10)
