import random
import time

from subprocess import check_output, CalledProcessError
from Queue import Queue
from threading import Thread
from datetime import datetime
from time import mktime


def write_file(file_path, data, mode='a+'):
    with open(file_path, mode) as file_write:
        file_write.write(data)


def append_tuple_data(init, tuple_data, delimiter):
    result_string = str(init) + delimiter
    for item in tuple_data:
        result_string += str(item) + delimiter
    return result_string + "\n"


def register_stats(iter, result_queue):
    stats_file_dir = "D:/stats/"
    # stats_file_dir="D:/"
    for index in range(result_queue.unfinished_tasks):
        tuple_data = result_queue.get(index)
        channel_id = "Channel_" + str(tuple_data[0])
        stats_file_path = stats_file_dir + channel_id + ".csv"

        data_write = append_tuple_data(iter, tuple_data, ";")

        write_file(stats_file_path, data_write, 'a+')
        result_queue.task_done()


def register_error(iteration, error_queue):
    error_file_path = "D:/Errors/Error.txt"
    # error_file_path = "D:/Error.txt"
    data_write = ""
    for index in range(error_queue.unfinished_tasks):
        tuple_data = error_queue.get(index)
        data_write += append_tuple_data(iteration, tuple_data, ";")
        error_queue.task_done()

    write_file(error_file_path, data_write, 'a+')


def random_date():
    format = '%m/%d/%Y %I:%M %p'
    start_date = "6/30/2016 4:00 PM"
    end_date = "6/30/2016 11:45 PM"
    stime = time.mktime(time.strptime(start_date, format))
    etime = time.mktime(time.strptime(end_date, format))

    ptime = stime + random.random() * (etime - stime)
    final_date = datetime.fromtimestamp(mktime(time.localtime(ptime)))

    return final_date


def build_command(channel_id,min):
    date_format = "%y%m%d"
    hour_format = "%H"
    min_format = "%M"
    timestamp_format = "%y%m%d_%H%M%S"
    channel_string = "{:0>2}".format(channel_id)

    rand_date = random_date()
    date_string = "160628"
    hour_string = "14"
    min_string = "{:0>2}".format(min)
    timestamp_string = str(datetime.now().strftime(timestamp_format))
    if (channel_id != 7):
        file_name = "WcT0768" + date_string + hour_string + min_string + "%02d_" + channel_string + ".jpg"
    else:
        file_name = "WcT0768" + date_string + hour_string + min_string + "%02d_05.jpg"
    input_file = "D:/civolution_test/Data/VideoThumbs/" + channel_string + "/" + date_string + "/" + hour_string + "/" + file_name
    output_file = "D:/Mp4Out2/" + channel_string + "/" + "ouput_" + timestamp_string + ".mp4"
    command = "ffmpeg -framerate 1 -i " + input_file + " -vcodec libx264 -pix_fmt yuv420p -r 10 -b:v 30k " + output_file + " -y -loglevel quiet"
    return command


def ffmpeg_worker(thread_queue, thread_result, error_queue):
    thread_data = thread_queue.get()
    try:
        thread_output = check_output(thread_data.get("task"), shell=True).decode()
        print(thread_output)
    except CalledProcessError:
        error_queue.put((thread_data.get("id"), thread_data.get("task")))

    thread_end_time = datetime.now()
    thread_exec_time = thread_end_time - thread_data.get("start_time")
    thread_result.put((thread_data.get("id"), thread_end_time, str(thread_exec_time)))
    thread_queue.task_done()


def main_process():
    thread_queue = Queue()
    thread_result = Queue()
    thread_error = Queue()
    # channel_range = range(1,6) + range(7, 9)

    for iteration in range(1,60):
        print("Round " + str(iteration))
        channel_range = [2]
        print(channel_range)
        for channel in channel_range:
            current_thread_name = channel
            current_thread_data = {"id": channel, "start_time": datetime.now(), "task": build_command(channel,min=iteration)}
            thread_queue.put(current_thread_data)
            current_thread = Thread(name=current_thread_name, target=ffmpeg_worker,
                                    args=(thread_queue, thread_result, thread_error))
            current_thread.daemon = False
            current_thread.start()

        thread_queue.join()
        thread_queue.empty()

        register_stats(iteration, thread_result)
        thread_result.empty()

        register_error(iteration, thread_error)
        thread_error.empty()

    print("End of execution")


if __name__ == "__main__":
    main_process()