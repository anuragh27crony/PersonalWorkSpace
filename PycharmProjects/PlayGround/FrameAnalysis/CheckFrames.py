import json
import subprocess
from subprocess import CalledProcessError

# subprocess.check_output(['ls','-l']) #all that is technically needed...
show_frames_command = 'ffprobe -print_format json -show_format -show_frames D:\\VV\\s0.ts'
show_packets_command = 'ffprobe -print_format json -show_format -show_packets D:\\VV\\s0.ts'

try:
    frames_output = json.loads(subprocess.check_output(show_frames_command))
    packets_output = json.loads(subprocess.check_output(show_packets_command))

    for frame in frames_output.get("frames"):
        if frame.get("media_type") == 'video':
            print "%s:%s:%s" % (
                frame.get("coded_picture_number"), frame.get("pkt_duration"), frame.get("pkt_duration_time"))

    print("============= PACKETS =============")
    counter = 0
    for packet in packets_output.get("packets"):
        if packet.get("codec_type") == "video":
            print "%s:%s:%s" % (counter, packet.get("duration"), packet.get("duration_time"))
            if counter == 1:
                print "Start Time:%s" % (packet.get("pts_time"))
            if counter == 104:
                print "End Time:%s" % (packet.get("pts_time"))
            counter += 1


except CalledProcessError:
    print("Process error reported")  # print(frames_output)
# print(packets_output)
