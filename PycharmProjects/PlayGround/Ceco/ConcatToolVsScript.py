import os
import shutil
import time

from subprocess import call, check_output
from datetime import timedelta, datetime
from Ceco.Utils import Utils
from Ceco import FpsUtil


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
            result_list.append(len(missing_ce))
            result_list.append(avg_ber_value)
            result_list.append(missing_ce)
            # result_list.append(result)
            self.write_results(self.results_dir, tuple(result_list), results_file_name)

    def create_concat_file(self, dir_path, files_list, suffix=None):
        file_name = "concat_tool_file"
        if suffix:
            file_name = file_name + str(suffix)
        concat_txt_file = os.path.join(dir_path, file_name + ".txt")
        for file_name in files_list:
            file_path = os.path.join(dir_path, file_name)

            with open(concat_txt_file, "a+") as file:
                file.writelines(file_path + "\n")
        return concat_txt_file


def fetch_base_dir(counter, ch_name):
    if counter == 0:
        base_dir = os.path.join("F:\\Dump\\CecoComparision\\NTSC\\", ch_name, "29-Oct")
    elif counter == 1:
        base_dir = os.path.join("E:\\Dump\\UDP\\07-nov\\", ch_name)
    else:
        if "rte2" in ch_name.lower():
            base_dir = os.path.join("D:\\Dump\\CecoComparision\\4.4-4.5\\PAL\\", ch_name, "06-Nov")
        elif len(ch_name) < 5:
            base_dir = os.path.join("D:\\Dump\\CecoComparision\\4.4-4.5\\PAL\\", ch_name, "04-Nov")
        else:
            base_dir = os.path.join("D:\\Dump\\CecoComparision\\4.4-4.5\\UDP\\", ch_name)
    return base_dir


ntsc_ch_list = ["rte2"]
udp_ch_list = ["cnews_f_1000", "tagg_f_1000"]
pal_ch_list = ["Re-Mux_Check_No_TS"]
bit_rates = [1800000]
counter = 2
vvcat_ver = "1.3.1.105"

for ch_list in [pal_ch_list]:
    for ch_name in ch_list:
        for bitrate in bit_rates:
            base_dir = fetch_base_dir(counter, ch_name)

            detec_ch_util = DetectorUtils(ch_name.lower())

            print(ch_name)
            print(base_dir)

            vids_dir = os.path.join(base_dir, "4.5_videos")
            concat_hour_vids_dir = os.path.join(vids_dir, "concat_hour_dir",
                                                "{0}_{1}".format(vvcat_ver, str(bitrate)))
            ref_ceco_dir = os.path.join(base_dir, "Ref_Cecos_crop_tool")
            concat_ref_ceco_dir = os.path.join(base_dir, "Ref_Cecos_crop_tool",
                                               "{0}_{1}".format(vvcat_ver, str(bitrate)))

            detec_ch_util.check_dir(ref_ceco_dir)
            detec_ch_util.check_dir(concat_ref_ceco_dir)
            detec_ch_util.check_dir(concat_hour_vids_dir)

            hourfile_prefix = "HourLong"
            concat_hourfile_prefix = "concat_HourLong"
            hour_dirs_list = detec_ch_util.list_files_dir(vids_dir)
            for hour_dir in hour_dirs_list:
                if "concat_hour_dir" not in hour_dir and int(hour_dir) > 0:
                    print(hour_dir)
                    hour_reading_str = "{0},{1},".format(ch_name, hour_dir)
                    hour_dir_path = os.path.join(vids_dir, hour_dir)

                    concat_hour_mp4_file = os.path.join(concat_hour_vids_dir,
                                                        concat_hourfile_prefix + hour_dir + ".mp4")
                    concat_out_put = os.path.join(concat_hour_vids_dir, concat_hourfile_prefix + hour_dir + ".log")
                    concat_hour_ref_ceco_file = os.path.join(concat_ref_ceco_dir,
                                                             concat_hourfile_prefix + hour_dir + ".ce")

                    try:
                        if not os.path.isfile(concat_hour_mp4_file):
                            concat_file_path = detec_ch_util.create_concat_file(hour_dir_path,
                                                                                detec_ch_util.list_files_dir(
                                                                                    hour_dir_path,
                                                                                    "mp4"),
                                                                                suffix=str(bitrate))

                            concat_start = time.time()
                            final_cmd = r"C:\tools\TtxVVcat\{0}\TtxVVcat.exe -i {1} -o {2} -c:v copy".format(
                                vvcat_ver,
                                concat_file_path,
                                concat_hour_mp4_file)
                            print(final_cmd)

                            with open(concat_out_put, "w") as log_stdout:
                                call(final_cmd, shell=True, stdout=log_stdout, stderr=log_stdout)
                            concat_time = time.time() - concat_start
                            hour_reading_str = hour_reading_str + "{0},".format(concat_time)

                    except Exception:
                        print("Error concat & removing path")

                    with open(os.path.join(os.getcwd(), "new_readings_2.txt"), "a+") as file:
                        file.writelines(hour_reading_str + "\n")
                    if not os.path.isfile(concat_hour_ref_ceco_file):
                        detec_ch_util.create_ref_ceco(concat_hour_mp4_file, concat_hour_ref_ceco_file)

                        # ingest_result = True
                        # csv_result = "{%s}_{%s}_{%s}" % (vvcat_ver, ch_name, str(bitrate))
                        #
                        # for ref_ceco in detec_ch_util.list_files_dir(concat_ref_ceco_dir, "ce"):
                        #     hour_dir = ref_ceco[-5:-3]
                        #     if "cnews_f_1000" in ch_name.lower() or "tagg_f_1000" in ch_name.lower():
                        #         date_obj = datetime.strptime('171107', '%y%m%d')
                        #     elif "rte2" in ch_name.lower():
                        #         date_obj = datetime.strptime('171106', '%y%m%d')
                        #     elif "rai1" in ch_name.lower():
                        #         date_obj = datetime.strptime('171104', '%y%m%d')
                        #     else:
                        #         date_obj = datetime.strptime("171029", '%y%m%d')
                        #     detec_ch_util.FpsUtil.clean_existing_feeds()
                        #     ingest_result = detec_ch_util.FpsUtil.ingest_ref_ceco(concat_ref_ceco_dir, ref_ceco,
                        #                                                           hour_dir + "0000")
                        #
                        #     if ingest_result:
                        #         candidate_ver = "C4.4"
                        #         candidate_ceco_dir = os.path.join(base_dir, "4.4_ceco", "collection")
                        #
                        #         candidate_ceco_file_list = detec_ch_util.candidate_ce_lst(date=date_obj, hour_str=hour_dir,
                        #                                                                   is_45=False)
                        #         detec_ch_util.analyze_candidate_cecos(candidate_ceco_dir, candidate_ceco_file_list,
                        #                                               candidate_ver,
                        #                                               "Ref4.5",
                        #                                               results_file_name=csv_result)
                        #
                        #         # candidate_ver = "C4.5"
                        #         # candidate_ceco_dir = os.path.join(base_dir, "4.5_ceco", "collection")
                        #         # candidate_ceco_file_list = detec_ch_util.candidate_ce_lst(date=date_obj, hour_str=hour_dir,
                        #         #                                                           is_45=True)
                        #         # detec_ch_util.analyze_candidate_cecos(candidate_ceco_dir, candidate_ceco_file_list,
                        #         #                                       candidate_ver,
                        #         #                                       "Ref4.5",
                        #         #                                       results_file_name=csv_result)
                        #
                        #         detec_ch_util.FpsUtil.restart_search_workers()
                        #         time.sleep(10)
                        # counter += 1
