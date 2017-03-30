import os
import subprocess as sp
import numpy
from pylab import *
import pylab
from matplotlib.pyplot import imshow

FFMPEG_BIN = "ffmpeg"
input_dir = "D:\\GitRepos\\PersonalWorkSpace\\IdeaProjects\\ZxingTest\\barcodes\\Videos_2_Check\\WcT0768170330115100_04.mp4"
output_dir = "D:"

input_file_path = os.path.join(input_dir, "filename")

# info_cmd = [FFMPEG_BIN, '-i', input_dir, '-']
# pipe = sp.Popen(info_cmd, stdout=sp.PIPE, stderr=sp.PIPE)
#
# pipe.stdout.readline()
# print(pipe.stderr.read())
# pipe.stdout.readline()
# print(pipe.stderr.read())
# pipe.terminate()

image_extract_cmd = [FFMPEG_BIN,
                     '-i', input_dir,
                     '-f', 'image2pipe',
                     '-pix_fmt', 'rgb24',
                     '-vcodec', 'rawvideo',
                     '-']

pipe = sp.Popen(image_extract_cmd, stdout=sp.PIPE, bufsize=10 ** 8)

raw_image = pipe.stdout.read(360 * 240 * 3)
print(type(raw_image))
image = numpy.fromstring(raw_image, dtype='uint8')
print(type(image))
image = image.reshape((240, 360, 3))
imshow(image)
pylab.show()

raw_image = pipe.stdout.read(360 * 240 * 3)
image = numpy.fromstring(raw_image, dtype='uint8')
image = image.reshape((240, 360, 3))
print("Before Printing")
imshow(image)
pylab.show()
print("Before Printing")
# throw away the data in the pipe's buffer.
pipe.stdout.flush()
