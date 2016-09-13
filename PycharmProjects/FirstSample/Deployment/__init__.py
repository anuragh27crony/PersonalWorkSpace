import os
import requests
from subprocess import check_output, CalledProcessError


def build_url(change_set, build_no):
    basic_url = 'http://cvl-bld-502.civolution.com/download/'
    arch = {'32': 'x32', '64': 'x64'}
    env = {'32': 'win32', '64': 'win64'}
    basic_build_name = 'setupTeletraxCVBSSVIDDetector_'

    os_bits = '32'
    if '64' in os.environ['PROCESSOR_ARCHITECTURE']:
        os_bits = '64'

    server_url = '%s%s/artifacts' % (basic_url, change_set)
    build_name = '%s%s_.4.1_64bits.BETA-%s.exe' % (basic_build_name, arch[os_bits], build_no)
    final_url = '%s/%s/%s' % (server_url, env[os_bits], build_name)
    return final_url


def download_build_return_file_path(url, username, password):
    http_resp = requests.get(url, auth=(username, password))
    installer_file_name = 'detector_installer.exe'
    installer_file_path = None

    if http_resp.status_code == 200:
        with open(installer_file_name, 'wb') as out:
            for bits in http_resp.iter_content():
                out.write(bits)
        installer_file_path = os.path.join(os.getcwd(),installer_file_name)
    else:
        print("Installer download failed with response code %s " % http_resp.status_code)

    return installer_file_path


def install_detector_silent(installer_file_path):
    if installer_file_path is not None:
        command = "%s /VERYSILENT /NORESTART /SUPPRESSMSGBOXES" % installer_file_path
        try:
            output = check_output(command)
        except CalledProcessError as e:
            print("error while installing detector %s " % e)
    else:
        print("Installer Path is empty")


changeset = 76227
build = 120761
user, password = '', ''

final_build_url = build_url(changeset, build)
print(final_build_url)
print(download_build_return_file_path(final_build_url, user, password))
