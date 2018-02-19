#!/usr/bin/python -u

import os
import sys
import tempfile
import subprocess

from optparse import OptionParser, IndentedHelpFormatter

class SettingsFile:    
    @staticmethod
    def open(name):
        """The purpose of that function is to aggregated differences between version python 2.5 
        on CentOS and python 2.6 for Windows platform. 
         Note when name is not equal to "" the tool will create file specifically for that. 
        """
        if name == "":
            if sys.platform == "win32":
                tmp_ini = tempfile.NamedTemporaryFile(delete=False)
            else:
                tmp_ini = tempfile.NamedTemporaryFile()
        else:
            tmp_ini = open(name, "w+")
        return tmp_ini

class Section:
    def __init__(self, name, enabled):
        self.name    = name 
        self.enabled = enabled

    def dump(self):
        if self.enabled == True:
            buffer  = "[%s]\n" % self.name
            for key in self.__dict__.keys():
                if key != 'name' and key != 'enabled':           
                    buffer += "%s=%s\n" % (key, self.__dict__[key])   
            return buffer
        else:
            return ""

version_info = ""

# INI file settings
config       = {}
config['General'] = Section('General', True)
config['General'].Input = 'Media'
config['General'].Output = 'CECO'

config['Logging'] = Section('General.Logging', True)
config['Logging'].EnableConsoleOutput=0
config['Logging'].EnableFileOutput=1
config['Logging'].OutputFile='FPToolGenerateCECO.log'
config['Logging'].OutputLevel=0

config['Media'] = Section('Media', True)
config['Media'].GenerationMode = 'Identification' # !!! should be identification
config['Media'].ProtectionMode = 'NoChecksum'

config['CECO'] = Section('CECO', True)
config['Constraint'] = Section('Media.Constraint', True)
config['Constraint'].Mode = 'Duration'
config['Constraint'].Duration = 10

CONTENT_DESCRIPTION='''<?xml version="1.0" encoding="UTF-8"?>
<FPMetadata>
    <First>%s</First>
    <Second>%s</Second>
    <Third>%s</Third>
    <Fourth>%s</Fourth>
</FPMetadata>

'''

if sys.platform == "win32":
    DEFAULT_ASSET_DESCRIPTION_SCHEMA=os.path.join(sys.path[0], "assetDescription.xsd")
else:
    DEFAULT_ASSET_DESCRIPTION_SCHEMA="/usr/share/fptool/assetDescription.xsd"

def main():     
    parser = OptionParser(formatter = IndentedHelpFormatter(width = 200, indent_increment=2, max_help_position=100))
    
    parser.add_option("-m", "--media",      action="store", dest="MediaFile",                type="string",  default="",    help="Media filename")
    parser.add_option("-t", "--mediatype",  action="store", dest="MediaType",                type="string",  default="",    help="Media type: music of movie, option is obsolete")
    parser.add_option("-u", "--algorithms", action="store", dest="Algorithms",               type="string",  default="",    help="Algorithm to use: VIDEO_ALGO_V5_4_65S, VIDEO_ALGO_V6_4_65S, AUDIO_ALGO_V5, user may specify multiple separating list with comma")    
    parser.add_option("-f", "--feature",    action="store", dest="Feature",                  type="int",     default=0,     help="Feature extraction (0 or 1).")    
    parser.add_option("--feature-version",  action="store", dest="FeatureVersion",           type="string",  default="VIDEO_FEATURES_V2",    help="Feature version to use: VIDEO_FEATURES_V2, VIDEO_FEATURES_V3")    
    parser.add_option("--assetdesc",        action="store", dest="AssetDescriptionFile",     type="string",  default="",    help="Asset description filename. When it is used, this option substitutes metadata1, metadata2, metadata3, metadata4 options.")
    parser.add_option("--schema",           action="store", dest="SchemaName",               type="string",  default=DEFAULT_ASSET_DESCRIPTION_SCHEMA, help="Schema used for validation of asset description (default: \"%default\")")
    parser.add_option("--metadata1",        action="store", dest="M1",                       type="string",  default="-",   help="Metadata1 (default: \"%default\")")
    parser.add_option("--metadata2",        action="store", dest="M2",                       type="string",  default="-",   help="Metadata2 (default: \"%default\")")
    parser.add_option("--metadata3",        action="store", dest="M3",                       type="string",  default="-",   help="Metadata3 (default: \"%default\")")
    parser.add_option("--metadata4",        action="store", dest="M4",                       type="string",  default="-",   help="Metadata4 (default: \"%default\")")
    parser.add_option("-c", "--ceco",       action="store", dest="CECOFilename",             type="string",  default="",    help="CECO filename")
    parser.add_option("--save",             action="store", dest="SaveSettings",             type="string",  default="",    help="Save settings to specified file")
    parser.add_option("--savedescription",  action="store", dest="SaveDescription",          type="string",  default="",    help="Save asset description to specified file")    
    parser.add_option("-a", "--appendopt",  action="store", dest="AdditionalOptions",        type="string",  default="",    help="Append additional options")
    parser.add_option("-v", "--version",    action="store_true", dest="VersionInfo",         help="Version information") 

    (options, args) = parser.parse_args()

    if options.VersionInfo:
        print( version_info)
        os._exit(0)

    if options.MediaFile == "":
        print( "Error: No media file was provided")
        os._exit(1)
    
    if not os.path.isfile(options.MediaFile):
        print( "Error: Unable to locate specified media file:", options.MediaFile)
        os._exit(1)
    
    Algorithms = options.Algorithms.split(',')
    for algo in Algorithms:
        if algo not in ["AUDIO_ALGO_V5", "VIDEO_ALGO_V5_4_65S", "VIDEO_ALGO_V6_4_65S"]:
            print( "Error: Incorrect or no algorithm is specified")
            os._exit(1)

    if options.Feature == 1:
        # Check feature version name
        if options.FeatureVersion not in ['VIDEO_FEATURES_V2', 'VIDEO_FEATURES_V3']:
            print( "Error: Incorrect feature version is specified")
            os._exit(1)

    if options.AssetDescriptionFile != "":        
        if not os.path.isfile(options.AssetDescriptionFile):
            print( "Unable to locate specified file:", options.AssetDescriptionFile)
            os._exit(1)
        if not os.path.isfile(options.SchemaName):
            print( "Unable to locate specified schema file:", options.SchemaName)
            os._exit(1)

    if options.CECOFilename == "":
        print( "Error: No filename provided for CECO file")
        os._exit(1)

    VideoTrackID = 0
    AudioTrackID = 0

    for algo in Algorithms:
        if algo in ["VIDEO_ALGO_V5_4_65S", "VIDEO_ALGO_V6_4_65S"]:
            AudioTrackID = 1

    config['Media'].Channels = ""
    for algo in Algorithms:
        config['Media'].Channels                = config['Media'].Channels + "," + algo
        config[algo]                            = Section('Media.Channel.'+algo, True)
        config[algo].Algorithm                  = algo
        config[algo].Compression                = 'Disabled'
        config[algo].Quality                    = 'Medium'
        config[algo].Source                     = options.MediaFile
         
        if algo == 'VIDEO_ALGO_V5_4_65S':
            config[algo].StreamNumber           = 1
            config[algo].Type                   = 'VIDEO_MEDIA'            
            config[algo].TrackID                = VideoTrackID
            if options.Feature == 1:
                config['Media'].Channels        = "%s,%s" % (config['Media'].Channels, options.FeatureVersion)
                config['Features']              = Section('Media.Channel.%s' % options.FeatureVersion, True)
                config['Features'].Algorithm    = options.FeatureVersion
                config['Features'].StreamNumber = config['VIDEO_ALGO_V5_4_65S'].StreamNumber
                config['Features'].Compression  = config['VIDEO_ALGO_V5_4_65S'].Compression
                config['Features'].Quality      = config['VIDEO_ALGO_V5_4_65S'].Quality
                config['Features'].TrackID      = config['VIDEO_ALGO_V5_4_65S'].TrackID
                config['Features'].Type         = config['VIDEO_ALGO_V5_4_65S'].Type            
                config['Features'].Source       = config['VIDEO_ALGO_V5_4_65S'].Source
        elif algo == 'VIDEO_ALGO_V6_4_65S':
            config[algo].StreamNumber           = 1
            config[algo].Type                   = 'VIDEO_MEDIA'            
            config[algo].TrackID                = VideoTrackID
            if options.Feature == 1:
                config['Media'].Channels        = "%s,%s" % (config['Media'].Channels, options.FeatureVersion)
                config['Features']              = Section('Media.Channel.%s' % options.FeatureVersion, True)
                config['Features'].Algorithm    = options.FeatureVersion
                config['Features'].StreamNumber = config['VIDEO_ALGO_V6_4_65S'].StreamNumber
                config['Features'].Compression  = config['VIDEO_ALGO_V6_4_65S'].Compression
                config['Features'].Quality      = config['VIDEO_ALGO_V6_4_65S'].Quality
                config['Features'].TrackID      = config['VIDEO_ALGO_V6_4_65S'].TrackID
                config['Features'].Type         = config['VIDEO_ALGO_V6_4_65S'].Type            
                config['Features'].Source       = config['VIDEO_ALGO_V6_4_65S'].Source
        else:
            config[algo].StreamNumber           = 0
            config[algo].Type                   = 'AUDIO_MEDIA'
            config[algo].TrackID                = AudioTrackID

    config['CECO'].OutputFilename = options.CECOFilename

    tmp_ini = SettingsFile.open(options.SaveSettings)
    tmp_content_decs = SettingsFile.open(options.SaveDescription)
    
    if options.AssetDescriptionFile == "":
        if options.M1 is not "-" or options.M2 is not "-" or options.M3 is not "-" or options.M4 is not "-":
            config['CECO'].AssetDescriptionFile = tmp_content_decs.name
            config['CECO'].ValidateAssetDescription = options.SchemaName
            tmp_content_decs.write(CONTENT_DESCRIPTION % (options.M1,
                                                          options.M2,
                                                          options.M3,
                                                          options.M4))
            tmp_content_decs.flush()
    else:
        config['CECO'].AssetDescriptionFile = options.AssetDescriptionFile 
        config['CECO'].ValidateAssetDescription = options.SchemaName
    
    for key in config.keys():
        if config[key].enabled == True:
            tmp_ini.write(config[key].dump())
            tmp_ini.write("\n");
    tmp_ini.flush()
    
    if sys.platform == "win32":
        rc = os.system("FPToolCmd.exe -i %s %s" % (tmp_ini.name, options.AdditionalOptions))    
    else:
        p = subprocess.Popen("FPToolCmd -i %s %s" % (tmp_ini.name, options.AdditionalOptions), shell=True)            
        rc = (os.waitpid(p.pid, 0)[1] >> 8)
        
    tmp_ini.close()
    os._exit(rc)

def check_environment():
    if sys.platform == "cygwin":
        print( "cannot be run in a cygwin environment, change your windows setup")
        sys.exit(1)
    else:
        min_version = (2,4)
        max_version = (2,7)
        if (sys.version_info[0],sys.version_info[1]) < min_version :
            print( "must be run with at least Python %d.%d" % (min_version[0],min_version[1]))
            sys.exit(1)
        if (sys.version_info[0],sys.version_info[1]) > max_version :
            print( "must be run with at most Python %d.%d" % (max_version[0],max_version[1]))
            sys.exit(1)

def check_cmd_installed():
    try:
        if sys.platform == "win32":
            proc = subprocess.Popen("FPToolCmd.exe -v", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.wait()
            version_info,error_info = proc.communicate()
        else:
            proc = subprocess.Popen("FPToolCmd -v", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            proc.wait()
            version_info,error_info = proc.communicate()
    except:
        print( "")
        print( "FPToolCmd executable cannot be found.")
        print( "Please check if it is installed and in the search path.")
        os._exit(1)

    return version_info
            
if __name__ == "__main__":
    check_environment()
    version_info = check_cmd_installed()
    main()
