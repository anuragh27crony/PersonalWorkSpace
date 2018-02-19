import csv
import os
import base64
import json

from Ceco import FpsNext
from dateutil import parser


class AnalyzeCeco:
    def __init__(self):
        self.fpsnext = FpsNext.FpsNext()

    def create_ceco_base64_str(self, ceco_file_path=None, encoded_file_output=None):
        with open(ceco_file_path, "rb") as ceco_file:
            encoded_string = base64.b64encode(ceco_file.read())

        if encoded_file_output is not None:
            with open(encoded_file_output, "w") as write_file:
                write_file.write(encoded_string)
        return encoded_string.decode("utf-8")

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
        search_analysis_result = json.loads(search_analysis_result)
        try:
            ce_elements = search_analysis_result.get("data").get("analysis").get("streams")[0].get("channels")[0].get(
                "contentElements")
            for ce in ce_elements:
                ce.update({"id": counter})
                counter += 1
            print(counter)
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

    def ingest_ref_ceco(self, ref_ceco_dir, ref_ceco_file_name=None, feed_id=None, meta_data=None):
        ingestion_succeeded = False
        if ref_ceco_file_name:
            ref_ceco_file_path = os.path.join(ref_ceco_dir, ref_ceco_file_name)
            if feed_id is None:
                print("ingesting: FeedId is empty")
                feed_id = ref_ceco_file_name

            print(ref_ceco_dir + "->" + ref_ceco_file_name + " : feedid" + feed_id)
            return_code = self.fpsnext.define_feed(feed_id=feed_id, request_meta_data=meta_data)
            if return_code and return_code > 199 and return_code < 300:
                try:
                    base64_ceco_str = self.create_ceco_base64_str(ceco_file_path=ref_ceco_file_path)
                    return_code = self.fpsnext.ingest_feed(feed_id=feed_id, ceco_data=base64_ceco_str)
                    ingestion_succeeded = True if return_code and return_code > 199 and return_code < 300 else False
                except FileNotFoundError as FNF:
                    print("Ref Ceco Missing")

        return ingestion_succeeded

    def analyze_candidate_ceco(self, candidate_ceco_dir, ceco_file_name=None):
        missing_zones = None
        result = None
        avg_ber_value = -1
        if ceco_file_name:
            candidate_ceco_file_path = os.path.join(candidate_ceco_dir, ceco_file_name)
            base64_ceco_str = self.create_ceco_base64_str(ceco_file_path=candidate_ceco_file_path)

            search_result = self.fpsnext.identify_feed(ceco_data=base64_ceco_str)
            (missing_zones, avg_ber_value, result) = self.analyze_search_result(search_result)

        return missing_zones, avg_ber_value, json.dumps(result)

    def analyze_ceco(self, ceco_file_name=None):
        if ceco_file_name is not None:
            candidate_ceco_file_path = os.path.join(self.candidate_ceco_dir, ceco_file_name)
            base64_ceco_str = self.create_ceco_base64_str(ceco_file_path=candidate_ceco_file_path)

            search_result = self.fpsnext.identify_feed(ceco_data=base64_ceco_str)
            return search_result

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

    def re_ingest_ref(self, ref_ceco_dir, ref_ceco_file_name, feed_id="201705"):
        try:
            self.clean_existing_feeds()
            feed_meta_data = {"metadata": feed_id, "maxBacklog": 3600000}
            self.ingest_ref_ceco(ref_ceco_dir, ref_ceco_file_name, feed_id=feed_id, meta_data=feed_meta_data)
        except Exception as e:
            print("re_ingest_ref: ")
            print(e)