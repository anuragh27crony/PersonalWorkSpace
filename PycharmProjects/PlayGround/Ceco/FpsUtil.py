import json
import os

from Ceco import FpsApi, CecoUtil


class FpsUtil:
    def __init__(self):
        self.fps_api_wrapper = FpsApi.FpsApi()
        self.ceco_utils = CecoUtil.CecoUtil()

    def ingest_ref_ceco(self, ref_ceco_dir, ref_ceco_file_name=None, feed_id=None, meta_data=None):
        ingestion_succeeded = False
        if ref_ceco_file_name:
            ref_ceco_file_path = os.path.join(ref_ceco_dir, ref_ceco_file_name)
            if feed_id is None:
                print("ingesting: FeedId is empty")
                feed_id = ref_ceco_file_name

            print(ref_ceco_dir + "->" + ref_ceco_file_name + " : feedid:" + feed_id)
            return_code = self.fps_api_wrapper.define_feed(feed_id=feed_id, request_meta_data=meta_data)
            if return_code and return_code > 199 and return_code < 300:
                try:
                    base64_ceco_str = self.ceco_utils.create_ceco_base64_str(ceco_file_path=ref_ceco_file_path)
                    return_code = self.fps_api_wrapper.ingest_feed(feed_id=feed_id, ceco_data=base64_ceco_str)
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
            try:
                search_result = self.analyze_ceco(candidate_ceco_file_path)
                (missing_zones, avg_ber_value, result) = self.ceco_utils.analyze_search_result(search_result)
            except Exception as e:
                print("Error in analyzing ceco {0}".format(candidate_ceco_file_path))
        else:
            print("Empty Ceco file name")

        return missing_zones, avg_ber_value, json.dumps(result)

    def analyze_ceco(self, ceco_file_path=None, is_analyze=False):
        if ceco_file_path:
            base64_ceco_str = self.ceco_utils.create_ceco_base64_str(ceco_file_path=ceco_file_path)
            search_result = self.fps_api_wrapper.identify_feed(ceco_data=base64_ceco_str, analyze_ceco=is_analyze)
            return search_result
        else:
            raise Exception

    def clean_existing_feeds(self):
        available_feeds_result = self.fps_api_wrapper.list_feeds()

        if available_feeds_result.get("success"):
            for feed in available_feeds_result.get("data"):
                self.fps_api_wrapper.delete_feed(feed.get("feedID"))

    def re_ingest_ref(self, ref_ceco_dir, ref_ceco_file_name, feed_id="201705"):
        try:
            self.clean_existing_feeds()
            feed_meta_data = {"metadata": feed_id, "maxBacklog": 3600000}
            self.ingest_ref_ceco(ref_ceco_dir, ref_ceco_file_name, feed_id=feed_id, meta_data=feed_meta_data)
        except Exception as e:
            print("re_ingest_ref: ")
            print(e)

    def restart_search_workers(self):
        self.fps_api_wrapper.restart_search_workers()
