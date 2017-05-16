import csv
import os
import base64
import FpsNext
import json

from dateutil import parser


class AnalyzeCeco:
    def __init__(self):
        self.ref_ceco_dir = "D:\CecoComparision\\4.3\\20170505\\00"
        self.candidate_ceco_dir = "D:\CecoComparision\\4.4\\20170505\\00"
        self.fpsnext = FpsNext.FpsNext()

    def create_ceco_base64_str(self, ceco_file_path=None, encoded_file_output=None):
        with open(ceco_file_path, "rb") as ceco_file:
            encoded_string = base64.b64encode(ceco_file.read())

        if encoded_file_output is not None:
            with open(encoded_file_output, "w") as write_file:
                write_file.write(encoded_string)
        return encoded_string

    def map_matching_zones(self, start_time, end_time, ce_elements):
        matching_ce_elements = list()

        for ce in ce_elements:
            ce_start_time = parser.parse(ce.get("start"))
            ce_end_time = parser.parse(ce.get("end"))
            ref_start_time = parser.parse(start_time)

            ref_end_time = parser.parse(end_time)
            if (ref_start_time <= ce_start_time) & (ref_start_time <= ce_end_time):
                if (ref_end_time >= ce_start_time) & (ref_end_time >= ce_end_time):
                    matching_ce_elements.append(ce.get("id"))

        return matching_ce_elements

    def missing_zones(self, ce_elements, results):
        zones = set()
        is_empty = True

        for ce in ce_elements:
            zones.add(ce.get("id"))

        if len(zones) > 0:
            is_empty = False

        for matching_block in results:
            zones.difference_update(set(matching_block.get("matchingZones")))

        if is_empty:
            print("Zones missing in Ceco")

        return zones

    def analyze_search_result(self, search_analysis_result=None):
        global final_result, missing_zones
        counter = 1
        avg_ber_value = -1

        try:
            ce_elements = search_analysis_result.get("data").get("analysis").get("streams")[0].get("channels")[0].get(
                "contentElements")
            for ce in ce_elements:
                ce.update({"id": counter})
                counter += 1

            counter = 0
            ber_values = list()
            for result in search_analysis_result.get("data").get("results"):
                matching_ce_zones = self.map_matching_zones(result.get("candidateStartUtc"),
                                                            result.get("candidateEndUtc"),
                                                            ce_elements)
                result.update({"matchingZones": matching_ce_zones})

                ber_values.append(result.get("berAverage") * len(matching_ce_zones))
                counter += len(matching_ce_zones)
            final_result = search_analysis_result.get("data").get("results")
            missing_zones = self.missing_zones(ce_elements, final_result)

            if counter == 0:
                print("Counter is Zeroo with Ber ")
                print(ber_values)
            else:
                avg_ber_value = (sum(ber_values) / float(counter))
        except AttributeError as ae:
            print("Attribute missing")

        return missing_zones, avg_ber_value, final_result

    def ingest_ref_ceco(self, ceco_file_name=None, feed_id=None, meta_data=None):

        if ceco_file_name is not None:
            ref_ceco_file_path = os.path.join(self.ref_ceco_dir, ceco_file_name)
            if feed_id is None:
                feed_id = ceco_file_name[7:17]
            base64_ceco_str = self.create_ceco_base64_str(ceco_file_path=ref_ceco_file_path)

            self.fpsnext.define_feed(feed_id=feed_id, request_meta_data=meta_data)
            self.fpsnext.ingest_feed(feed_id=feed_id, ceco_data=base64_ceco_str)

    def analyze_candidate_ceco(self, ceco_file_name=None):
        # candidate_detec_id = candidate_ceco_file[3:7]
        missing_zones = None
        result = None
        avg_ber_value = -1
        if ceco_file_name is not None:
            candidate_ceco_file_path = os.path.join(self.candidate_ceco_dir, ceco_file_name)
            base64_ceco_str = self.create_ceco_base64_str(ceco_file_path=candidate_ceco_file_path)

            search_result = self.fpsnext.identify_feed(ceco_data=base64_ceco_str)
            (missing_zones, avg_ber_value, result) = self.analyze_search_result(search_result)

        return missing_zones, avg_ber_value, json.dumps(result)

    def clean_existing_feeds(self):
        available_feeds_result = self.fpsnext.list_feeds()

        if available_feeds_result.get("success"):
            for feed in available_feeds_result.get("data"):
                self.fpsnext.delete_feed(feed.get("feedID"))

    def ceco_aggr(self, source_dir=None):
        import glob, os, shutil
        dest_dir = os.path.join(source_dir, "aggr")

        if not os.path.isdir(dest_dir):
            os.mkdir(dest_dir)

        os.chdir(source_dir)

        for folder in os.listdir(source_dir):
            if "Aggr" not in folder.title():
                files = glob.iglob(os.path.join(folder, "*.ce"))
                for file in files:
                    print(os.path.join(source_dir, file) + "->" + file.title())
                    if os.path.isfile(file) and "Aggr" not in file.title():
                        shutil.copy2(os.path.join(source_dir, file), dest_dir)

    def re_ingest_ref(self):
        try:
            self.clean_existing_feeds()
            ref_ceco_file = "24_Media2CECO_6-FLV-001.ceco"
            self.ref_ceco_dir = os.path.join("D:", os.sep)
            feed_meta_data = {"metadata": "ReferenceFileNed1.ts", "maxBacklog": 3600000}
            self.ingest_ref_ceco(ref_ceco_file, feed_id="201705", meta_data=feed_meta_data)
        except Exception as e:
            print("re_ingest_ref: ")
            print(e)


def write_results(data, detec_version=None):
    file_name = "D:\\CecoComparision\\results\\result-weighted_ber-" + detec_version + ".csv"

    with open(file_name, 'a+') as csv_file:
        cw = csv.writer(csv_file)
        cw.writerow(list(data))


versions = ["4.3", "4.4"]
analyze = AnalyzeCeco()
# analyze.ceco_aggr(source_dir="D:\\CecoComparision\\4.3-20170507")
# analyze.ceco_aggr(source_dir="D:\\CecoComparision\\4.4-20170507")

for version in versions:
    analyze.re_ingest_ref()
    if version in "4.3":
        analyze.candidate_ceco_dir = os.path.join("D:\CecoComparision\\4.3-20170507\\aggr")
    else:
        analyze.candidate_ceco_dir = os.path.join("D:\CecoComparision\\4.4-20170507\\aggr")

    for candidate_ceco_file in os.listdir(analyze.candidate_ceco_dir):
        detec_id = candidate_ceco_file[3:7]
        channel_id = candidate_ceco_file[-5:-3]
        (missing_ce, avg_ber_value, result) = analyze.analyze_candidate_ceco(candidate_ceco_file)
        write_results(
            (version, detec_id, channel_id, candidate_ceco_file, avg_ber_value, len(missing_ce), missing_ce, result),
            detec_version=version)

        if not len(result) > 2:
            analyze.re_ingest_ref()
            (missing_ce, avg_ber_value, result) = analyze.analyze_candidate_ceco(candidate_ceco_file)
            write_results((version, detec_id, channel_id, candidate_ceco_file, avg_ber_value, len(missing_ce),
                           missing_ce, result),
                          detec_version=version)
