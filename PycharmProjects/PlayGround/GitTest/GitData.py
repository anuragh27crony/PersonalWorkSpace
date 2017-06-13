import json
import platform
import os
import re
import xml.etree.ElementTree as ET

from datetime import datetime
from github import Github


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
    print(robot_xml_file_path)
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


def fetch_build_no(filepath):
    build_num = "0000000"

    try:
        with open(filepath, 'r') as file:
            data = file.readline()
            build_num_unformatted = data.split("build")[1].split(",")[0]
            build_num = re.sub(r"\s+", "", build_num_unformatted, flags=re.UNICODE)
    except Exception as e:
        pass

    return build_num


def prepare_env_data(computer_name, build_no, product=''):
    if 'Windows' in platform.system():
        os = '%s %s' % (platform.system(), platform.uname()[2])
    else:
        os = '%s %s' % (platform.linux_distribution()[0][:6], platform.linux_distribution()[1])


    if 'pcd' in product:
        ref_env_data = {'CVL-WST-073': {'mode': 'Osprey', 'os': '2008 Web'},
                        'WIN-8OP8KJL1788': {'mode': 'Osprey', 'os': '2008 Standard'},
                        'WIN-L3VBJI5833L': {'mode': 'Osprey', 'os': '2012 Standard'},
                        'WIN-7ILHV9HS7D5': {'mode': 'Matrox', 'os': '2008 Standard'},
                        'ComputerName': {'mode': 'Matrox', 'os': '2008 Web'},
                        'WIN-FFMBDF8D2S2': {'mode': 'UDP', 'os': '2012 Standard'}}
        data = ref_env_data.get(computer_name)
    else:

        data = {'mode': 'cmd', 'os': os}
    try:
        env_details = dict()

        for key, value in data.items():
            env_details.update({key: value})

        if '64' in platform.machine():
            env_details.update({"osbits": "64"})
        else:
            env_details.update({"osbits": "32"})

        time = datetime.now()
        env_details.update({"time": time.isoformat(' ')})
        env_details.update({"build": build_no})

        file_name = env_details.get("mode") + "_" + ''.join(env_details.get("os").split()) + "_" + str(
            build_no) + '_' + time.strftime('%y_%m_%d_%H_%M_%S')
        env = {"env": env_details, "file_name": file_name}

    except KeyError as e:
        print("Exception :Fetching env details", e)

    return env


def write_file(data, file_path, is_data_json=False):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    try:
        with open(file_path, "w+") as file_write:
            if is_data_json:
                file_write.write(json.dumps(data))
            else:
                file_write.write(data)
    except Exception as e:
        print("Exception Occured writing file %s, %s" % (file_path, e))


def prepare_graph_data(metadata, robot_data_dict):
    graph_data = dict(metadata)
    graph_data.update(robot_data_dict)
    return graph_data


def write_content_github(data, relative_file_path, commit_message):
    git_obj = Github('AnuragMala', 'Amullu124!@$')
    repo_obj = git_obj.get_organization('Teletrax').get_repo('RobotReports')
    commit_response = repo_obj.create_file(path=relative_file_path, message=commit_message, content=data)
    return commit_response


def upload_results_github(robot_xml_file_path=None,
                          artifacts_dir=os.path.join(".", "artifacts"), build_number=None,
                          detector_install_dir=os.path.join("D:", "civolution"), product=""):
    if build_number is None:
        # Fetch installed build
        build_no = fetch_build_no(os.path.join(detector_install_dir, 'AuthorizationCode.txt'))
    else:
        build_no = build_number

    git_artifacts_dir = os.path.join(artifacts_dir, "git")
    git_run_artifacts_dir = os.path.join(git_artifacts_dir, "run")

    # Prepare Env metadata
    env_metadata = prepare_env_data(os.environ.get('computername'), build_no)
    file_name = env_metadata.pop("file_name") + '.json'

    if robot_xml_file_path is not None:
        try:
            # Extract json out of Robot XML file (Stats & Test-case details)
            robot_data = extract_execution_stats(robot_xml_file_path)

            # FailSafe: Persist Data before git upload
            graph_data = prepare_graph_data(env_metadata, robot_data)
            write_file(graph_data, file_path=os.path.join(git_run_artifacts_dir, file_name), is_data_json=True)

            # Upload stats data to Git
            git_relative_path = "/".join(('', product, 'stats/history', str(build_no), file_name))
            git_commit_message = "Automation of Build: %s  - File: %s" % (str(build_no), file_name)
            response = write_content_github(data=json.dumps(graph_data), relative_file_path=git_relative_path,
                                            commit_message=git_commit_message)
            print(response)
            # Persist Git's Response in event of Failure
            # write_file(response, file_path=os.path.join(git_artifacts_dir, "git_commit_response.txt"), is_data_json=True)
        except Exception as e:
            print("Exception occured Read & Upload results to git %s", e)
    else:
        print("Exception Robot xml file is none: %s", robot_xml_file_path)


# json_data=extract_execution_stats(os.path.join(os.getcwd(), "Data", "2016-11-08_075935_output_FPTool_Rerun.xml"))
# print(json.dumps(json_data))

xml_file = os.path.join(os.getcwd(), "Data", "2016-11-08_075935_output_FPTool_Rerun.xml")
upload_results_github(robot_xml_file_path=xml_file, build_number='4.1', product='Fptool')
