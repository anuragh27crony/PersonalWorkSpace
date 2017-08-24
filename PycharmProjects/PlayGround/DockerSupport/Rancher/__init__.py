import os
import ruamel.yaml as yaml


class DockerComposeFileCreation:
    def __init__(self):
        self.docker_compose_dict = {'version': '2'}

    def add_a_service(self, new_service):
        is_success = False
        try:
            updated_services_list = [new_service]

            # Add/append existing services
            if self.docker_compose_dict.get("services") is not None:
                updated_services_list.extend(self.docker_compose_dict.get("services"))

            self.docker_compose_dict.update({"services": updated_services_list})

            is_success = True
        except Exception as e:
            print(e)

        return is_success

    def add_detector(self, detector_id, ch_str_list=None, max_recording_date='2014-02-02',
                     dwld_mgr_endpoint="detector.vagrant.teletrax.com",
                     extra_hosts='detector.vagrant.teletrax.com:192.168.214.178'):

        is_success = False
        try:
            # Incase of empty channel list, populate with 1-8 channels.
            if not ch_str_list or ch_str_list is None:
                ch_str_list = ",".join("{:02d}".format(x) for x in range(1, 9))

            detector = {detector_id:
                            {'image': 'registry.teletrax.biz/ttx/videoproviderservice:latest',
                             'environment':
                                 {'CHANNEL_LIST': ch_str_list,
                                  'DATE': max_recording_date,
                                  'DETECTOR_ID': detector_id,
                                  'SERVER_URL': dwld_mgr_endpoint,
                                  'SLEEP': '1'},
                             'volumes':
                                 ['/data:/opt/video-provider-service/data'],
                             'extra_hosts':
                                 [extra_hosts]
                             }
                        }
            is_success = self.add_a_service(detector)
        except Exception as e:
            print(e)
        return is_success

    def add_rabbitmq(self, mgmt_username='admin', mgmt_pass='admin',
                     queue_mgmt_ports=None):
        is_success = False
        try:
            # Queue & Mgmt port check for rabbitMQ
            if queue_mgmt_ports is None:
                queue_mgmt_ports = ['5672:5672/tcp', '15672:15672/tcp']

            rabbit_mq = {
                'rabbit':
                    {'image': 'rabbitmq:3.6-management',
                     'environment':
                         {'RABBITMQ_DEFAULT_PASS': mgmt_username,
                          'RABBITMQ_DEFAULT_USER': mgmt_pass},
                     'ports':
                         queue_mgmt_ports
                     }
            }
            is_success = self.add_a_service(rabbit_mq)
        except Exception as e:
            print(e)

        return is_success

    def get_compose_string(self, indent=2):
        return yaml.dump(self.docker_compose_dict, Dumper=yaml.RoundTripDumper, indent=indent)

    def write_compose_file(self, filepath=None, filename=""):

        if filepath is None:
            filepath = os.path.curdir

        if not os.path.exists(filepath):
            try:
                os.makedirs(filepath)
            except FileExistsError:
                print("File Exists")

        if ".yml" not in filename:
            filename += ".yml"
        try:
            docker_compose_str = self.get_compose_string()
            with open(os.path.join(filepath, filename), "w+") as compose_file:
                compose_file.write(docker_compose_str)

        except Exception as e:
            print("Exception occurred")
            print(e)


dcf = DockerComposeFileCreation()
print(dcf.add_rabbitmq())
print(dcf.add_detector(detector_id="0T68"))
print(dcf.get_compose_string())
dcf.write_compose_file(filename="test.yml")
