from _winreg import OpenKey, HKEY_LOCAL_MACHINE, ConnectRegistry, EnumValue, QueryInfoKey, QueryValue, QueryValueEx

aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)

with OpenKey(aReg,r"SOFTWARE\Teletrax\C:/civolution") as key:
    # print(EnumValue(key,0))
    # print(QueryInfoKey(key))
    # print(QueryValueEx(key,"Uninstall"))
    print(QueryValueEx(key,"AudioDeviceFilter"))
    print(dir(QueryValueEx(key,"AudioDeviceFilter")))



    # with OpenKey(aReg,r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run") as key:
#     print(key)