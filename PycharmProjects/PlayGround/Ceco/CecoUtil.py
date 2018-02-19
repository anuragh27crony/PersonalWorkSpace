import base64
import json

from dateutil import parser


class CecoUtil:
    def __init__(self):
        pass

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
