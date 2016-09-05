import os,sys

# print(os.sep)
# print(__file__)


ThisScript = os.path.abspath(__file__)
Anchor = os.sep + "Testing" + os.sep
AnchorPath = ThisScript[:ThisScript.rfind(Anchor) + len(Anchor)]
sys.path.append(AnchorPath)

print(Anchor)
print(ThisScript)
print(AnchorPath)


    # import config.applicationConfigurator as appCfg
    # appCfg.configure_all(__file__)