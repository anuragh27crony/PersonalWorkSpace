import binascii
import calendar
from struct import unpack

from datetime import datetime


def read_header_metadata(ceco_file):
    ceco_header = ceco_file.read(8)
    header = unpack("<4sHbb", ceco_header)
    print("tag, ceco_type, version_minor, version_major")
    print(header)

    extended_ceco_header = ceco_file.read(56)
    CECO_flags, CECO_CRC32 = unpack("<II", extended_ceco_header[0:8])
    print("ceco flag for crc", CECO_flags)
    print("crc value is ", CECO_CRC32)

    ceco_crc32 = binascii.crc32(ceco_header)
    ceco_crc32 = binascii.crc32(extended_ceco_header[0:4], ceco_crc32)
    ceco_crc32 = binascii.crc32(extended_ceco_header[8:], ceco_crc32)
    print("crc calculated", ceco_crc32)

    meta_mediainfoSize = ceco_file.read(4)
    meta_mediainfo_size, = unpack("<L", meta_mediainfoSize)
    meta_mediainfo = ceco_file.read(meta_mediainfo_size)
    print("meta mediainfo size", meta_mediainfo_size)

    # <?xml version="1.0" encoding="UTF-8" standalone="no" ?>
    #   <AssetInfo>
    #       <Stream Number="1" Type="Video">
    #           <Channel Algo="VIDEO_ALGO_V5_4_65S"/>
    #       </Stream>
    # </AssetInfo>
    print(meta_mediainfo)

    contentdescriptionSize = ceco_file.read(4)
    contentdescription_size, = unpack("<L", contentdescriptionSize)
    contentdescription = ceco_file.read(contentdescription_size)
    print("Meta Content Desc size", contentdescription_size)

    # <FPMetadata>
    #   <PCDetectorVersion>
    #       /BroadcastMonitoring/CVBS-SVIDDetector/Branches/4.1_64bits.BETA.120214
    #   </PCDetectorVersion>
    # </FPMetadata>
    print(contentdescription)


def HRTimestamp(civ_msec):
    # convert fromCiv epoch msec to Human Readable date time

    # civ msec (civ epoch) -> utc msec (epoch)
    y2k = 2000, 1, 1, 0, 0, 0
    civepoch_msec = calendar.timegm(y2k) * 1000
    utc_msec = civ_msec + civepoch_msec

    # msec to data time.
    msec_only = utc_msec - ((utc_msec // 1000) * 1000)
    dt = datetime.datetime.utcfromtimestamp(utc_msec // 1000)
    hrtime = dt.strftime('%Y %m %d %H:%M:%S') + "." + str(msec_only)

    return hrtime


# ceco_file = open("C:\WcD07681607190705_01.ce", "rb")
# read_header_metadata(ceco_file)
#
# data_size=ceco_file.read(4)
# ce_size,=unpack("<L",data_size)
# print("ce size",ce_size)
#
# ce=ceco_file.read(ce_size)
# ce_header_size = 64
# ce_header_set=(ce_type, ce_version, ce_timestamp, ce_duration, ce_streamnumber, ce_flags, ce_algo_version, ce_crc, ce_data_len) = unpack("<bIQQIIIII", ce[0:ce_header_size - 23])
# print(ce_header_set)
# print("ce timestamp",ce_timestamp)
# print(HRTimestamp(ce_timestamp))
#
# ai=0
# size=2048
# test=(ai <= size - 2048)
# blocklen = (ai <= size - 2048) and 1024
# blocklen2=blocklen  or (size - ai) / 2
# print(test and 100)
# print(blocklen)
# print(blocklen2)

def create_detec_filename(datetime, mac_id, channel_index, is_ceco=False, is_qsd=False, timestamp_bruned=True):
    filename = list()
    if is_ceco:
        filename.append("WcD")
        time_formatter = "%y%m%d%H%M"
        file_ext = ".ce"
    else:
        filename.append("Wt") if timestamp_bruned else filename.append("Wv")
        filename.append("Q") if is_qsd else filename.append("V")
        time_formatter = "%y%m%d%H%M%S"
        file_ext = ".mp4"

    filename.append(
        "{0}{1}_{2}{3}".format(str(mac_id).upper(), datetime.strftime(time_formatter), channel_index, file_ext))

    return ''.join(filename)


timestamp = datetime.strptime("2017-10-11", '%Y-%m-%d')
print(create_detec_filename(timestamp, "0a00", "01"))
print(create_detec_filename(timestamp, "0a00", "01",is_qsd=True))
print(create_detec_filename(timestamp, "0a00", "01", is_ceco=True))
