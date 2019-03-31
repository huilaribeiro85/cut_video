import os
import subprocess
import time
import _thread as thread
from cut_processor.cut_processor import web_server, video_processor, log_reader

logs_path = os.path.join(os.getcwd(), "logs")
videos_to_process_path = os.path.join(os.getcwd(), r"videos_to_process")
processed_videos_path = os.path.join(os.getcwd(), r"processed_videos")


def run_web_server():
    web_server_path = os.path.abspath(web_server.__file__)
    subprocess.run(["python", web_server_path])


def run_video_processor():
    video_processor.VideoProcessor(logs_path, videos_to_process_path, processed_videos_path).run()


thread.start_new_thread(run_web_server)
thread.start_new_thread(run_video_processor)

log = ""
while True:
    time.sleep(10)
    start_log_reader = log_reader.GetLog(logs_path).run()
    if start_log_reader and log != start_log_reader:
        log = start_log_reader
        print(start_log_reader)
