# from winreg import OpenKey, HKEY_LOCAL_MACHINE, QueryValueEx
#
# # with OpenKey(HKEY_LOCAL_MACHINE,r"SOFTWARE\Teletrax\C:/civolution") as key:
# #     print(QueryValueEx(key,"AudioDeviceFilter"))
# #     print(dir(QueryValueEx(key,"AudioDeviceFilter")))
#
# with OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Teletrax\TeletraxCVBSSVIDDetector") as key:
#     (uninstall_path, index) = QueryValueEx(key, "Uninstall")
#     install_dir = uninstall_path[:2]
# #     print(install_dir)
#
# import platform
# print(platform.platform())


import datetime

def UtcNow():
    now = datetime.datetime.utcnow()
    print(now)
    return now

UtcNow()