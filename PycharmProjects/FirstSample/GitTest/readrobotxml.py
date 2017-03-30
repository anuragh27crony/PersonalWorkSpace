import xml.etree.ElementTree as ET
import os
import json


class TestCase(object):
    def __init__(self):
        self.status = 'No RUN'
        self.name = ''
        self.start_time = ''
        self.end_time = ''

    def jsonify(self):
        return dict({'name': self.name, 'status': self.status, 'start': self.start_time, 'end': self.end_time})


class TotalRunDetails(object):
    def __init__(self):
        self.test_case_list = []
        self.total_pass_count = 0
        self.total_fail_count = 0

    def jsonify(self):
        self.total_tests = self.total_fail_count + self.total_pass_count
        return dict({'aggr': {'pass': self.total_pass_count, 'fail': self.total_fail_count, 'total': self.total_tests},
                     'scenarios': self.test_case_list})


def extract_execution_stats(robot_xml_file_path):
    total_run_details = TotalRunDetails()
    for event, elem in ET.iterparse(source=robot_xml_file_path, events=('start', 'end')):
        if event == 'end':
            if elem.tag == 'test':
                test_case = TestCase()
                test_case.name = elem.attrib.get("name")
                for node in elem.getchildren():
                    if node.tag == 'status':
                        test_case.status = node.attrib.get("status")
                        test_case.start_time = node.attrib.get("starttime")
                        test_case.end_time = node.attrib.get("endtime")
                total_run_details.test_case_list.append(test_case.jsonify())

        if event == 'start':
            if elem.tag == 'total':
                for node in elem.getchildren():
                    if node.text.lower() == 'all tests':
                        total_run_details.total_pass_count = int(node.attrib.get("pass"))
                        total_run_details.total_fail_count = int(node.attrib.get("fail"))

    return total_run_details.jsonify()


# print(json.dumps(extract_execution_stats('2016-09-16_133945_output_4.3.xml')))


def write_file(data, file_path, is_data_json=False):
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path))
    else:
        print(os.path.exists(file_path))

    try:
        with open(file_path, "w+") as file_write:
            if is_data_json:
                file_write.write(json.dumps(data))
            else:
                file_write.write(data)
    except Exception as e:
        print("Exception Occured", e)


print(os.path.abspath(os.path.join("..", "artifacts", "git", "filename3.txt")))
# write_file("testing is fun", file_path=os.path.join("..", "artifacts", "git", "filename3.txt"))


def fetch_build_no(filepath):
    with open(filepath, 'r') as file:
        data = file.readline()
        return data.split("build")[1].split(",")[0]

#
# file_name='AuthorizationCode.txt'
# file_path=os.path.join(os.getcwd(),file_name)
# print(file_path)
# print(read_build(file_path))
