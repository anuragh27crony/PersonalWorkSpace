import os

from qtfaststart import processor


def with_out_fps(root_dir):
    for dir_path, subdirList, fileList in os.walk(root_dir):
        path_split = dir_path.split("\\")[-1:]
        print(path_split)
        print(','.join(path_split[0].split("_")))

        for file_name in fileList:
            abs_file_path = os.path.join(dir_path, file_name)
            index = processor.get_index(open(abs_file_path, "rb"))

            for atom, pos, size in index:
                if atom == "\x00\x00\x00\x00":
                    atom = "----"
                if "moov" in str(atom):
                    print("%s %s" % (file_name, str(size)))


def with_fps(root_dir):
    for dir_path, subdirList, fileList in os.walk(root_dir):
        print(','.join(dir_path.split("//")[-1:][0].split("_")))

        for file_name in fileList:
            abs_file_path = os.path.join(dir_path, file_name)
            index = processor.get_index(open(abs_file_path, "rb"))

            for atom, pos, size in index:
                if atom == "\x00\x00\x00\x00":
                    atom = "----"
                if "moov" in str(atom):
                    print("%s" % (str(size)))


# root_dir = "D:\\AtomTesting\\Without_FPS"
# with_out_fps(root_dir)

root_dir = "C://Users//amala//Desktop//MoovAtom//"
with_fps(root_dir)
