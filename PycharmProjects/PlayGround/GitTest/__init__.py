import glob
import os
import timeit


def glob_search(channel):
    print("===== GLOB =====")
    start_time = timeit.default_timer()
    lastCreatedFile = ""

    if channel != 0:
        searchPattern = "*" + str(channel) + ".ce"
    else:
        searchPattern = "*.ce"

    path = os.path.join("C:\\civolution", 'Data')

    cecoFiles = None
    if os.path.isdir(path):
        cecoFiles = glob.glob(path + os.sep + searchPattern)
        cecoFiles.sort(key=lambda f: os.path.getmtime(os.path.join(path, f)), reverse=True)

        if len(cecoFiles) > 0:
            lastCreatedFile = cecoFiles[0]

    end_time = timeit.default_timer()
    print(os.path.join(path, lastCreatedFile) + "-->" + str(len(cecoFiles)) + "-->" + str(end_time - start_time))


def os_list_way(channel=None, file_ext=None):
    print("===== OS LIST DIR =====")
    start_time = timeit.default_timer()
    lastCreatedFile = ""

    if channel != 0:
        searchPattern = "*" + str(channel) + str(file_ext)
    else:
        searchPattern = "*" + str(file_ext)

    path = os.path.join("D:\\civolution", 'Data')

    cecoFiles = None
    if os.path.isdir(path):
        cecoFiles = glob.glob(path + os.sep + searchPattern, recursive=False)
        cecoFiles.sort(reverse=True)

        for dirfile in cecoFiles:
            with open('filenames.txt', 'a+') as datafile:
                datafile.write(dirfile + "\n")

        if len(cecoFiles) > 0:
            lastCreatedFile = cecoFiles[0]

    end_time = timeit.default_timer()
    print(os.path.join(path, lastCreatedFile) + "-->" + str(len(cecoFiles)) + "-->" + str(end_time - start_time))


os_list_way(0, ".ttx")
os_list_way(0, ".ce")
os_list_way(0, ".srt")
