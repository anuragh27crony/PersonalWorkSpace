from _winreg import OpenKey, HKEY_LOCAL_MACHINE, QueryValueEx

with OpenKey(HKEY_LOCAL_MACHINE,r"SOFTWARE\Teletrax\C:/civolution") as key:
    print(QueryValueEx(key,"AudioDeviceFilter"))
    print(dir(QueryValueEx(key,"AudioDeviceFilter")))