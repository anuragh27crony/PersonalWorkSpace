import random
import multiprocessing as mp
import time
from time import mktime
from datetime import datetime
#
# def strTimeProp(start, end, format, prop):
#     stime = time.mktime(time.strptime(start, format))
#     etime = time.mktime(time.strptime(end, format))
#
#     ptime = stime + prop * (etime - stime)
#
#     return time.strftime(format, time.localtime(ptime))
#
#
# def randomDate(start, end, prop):
#     return strTimeProp(start, end, '%m/%d/%Y %I:%M %p', prop)
#
# print randomDate("1/1/2008 1:30 PM", "1/1/2009 4:50 AM", random.random())
#
#
# def random_date():
#     format='%m/%d/%Y %I:%M %p'
#     start_date="6/18/2016 1:00 AM"
#     stime = time.mktime(time.strptime(start_date, format))
#     etime = time.mktime(time.localtime(time.time()-86400))
#
#     ptime = stime + random.random() * (etime - stime)
#     final_date = datetime.fromtimestamp(mktime(time.localtime(ptime)))
#
#     return final_date
#
#
# def build_command(channel_id):
#     date_format = "%y%m%d"
#     hour_format = "%H"
#     min_format = "%M"
#     timestamp_format="%y%m%d_%H%M%S"
#     channel_string="{:0>2}".format(channel_id)
#
#     rand_date = random_date()
#     date_string = str(rand_date.strftime(date_format))
#     hour_string = str(rand_date.strftime(hour_format))
#     min_string = str(rand_date.strftime(min_format))
#     timestamp_string = str(datetime.now().strftime(timestamp_format))
#     if(channel_id!=7):
#         file_name="WcT0768"+date_string+hour_string+min_string+"%02d_"+channel_string+".jpg"
#     else:
#         file_name = "WcT0768" + date_string + hour_string + min_string + "%02d_05.jpg"
#     input_file = "D:/civolution/Data/VideoThumbs/"+channel_string+"/"+date_string+"/"+hour_string+"/"+file_name
#     output_file = "D:/Mp4Output/"+channel_string+"/"+"ouput_"+timestamp_string+".mp4"
#     command = "ffmpeg -framerate 1 -i "+input_file+" -vcodec libx264 -pix_fmt yuv420p -r 10 -b:v 15k "+output_file+" -y -loglevel quiet"
#     return command
#
#
#
# channel_range = range(1,6) + range(7, 9)
# for x in channel_range:
#     print(build_command(x))
# from Queue import Queue
# result=Queue()
#
# for x in range(10):
#     result.put((x,((x*100)+21)))
#
# for data in iter(result.get,None):
#     print data

print(int(random.random()*5+1))
print(random.random())
print(random.random())

#ffmpeg -r 1 -i WcT07681606070821%02d_01.jpg -pix_fmt yuv420p -r 10 -b:v 15k <output_filename>.mp4 -y

# D:\civolution\Data\VideoThumbs\03\160621\00\WcT0768-160621-00-00-03_03
#
#
#
#
# pool = mp.Pool(7)
# results = pool.map(time.sleep, [4, 6, 8] )
#
#
# import time
# from datetime import datetime
# ticks=time.time()
# cputicks=time.clock()
#
# print("cpu ticks "+str(cputicks))
# print("ticks "+str(ticks))
# print("asctime "+str(time.ctime(ticks)))
#
# localtime=time.localtime(ticks)
# print(localtime)
# print(time.asctime(localtime))
#
# start=datetime.now()
# # time.sleep(5)
# end=datetime.now()
# # print("difference "+str(end-start))
#
# print(end.hour)
# print(end.minute)
# print(end.second)
# print("{:0>2}".format(end.day))
# print("{:0>2}".format(end.month))
# print(end.year)
# format = "%Y%m%d"
# format2 = "%H%M%S"
# format3 = "%H%M"
# print(end.strftime(format))
# print(end.strftime(format2))
# print(end.strftime(format3))
#
#
