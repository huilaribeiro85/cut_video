import os
import subprocess
import time
import _thread as thread
from cut_processor.cut_processor import web_server, video_processor, log_reader

class Processor():
    def __init__(self, log_path=os.path.join(os.getcwd(), "logs"),
                 videos_to_process_path=os.path.join(os.getcwd(), r"videos_to_process"),
                 processed_videos_path=os.path.join(os.getcwd(), r"processed_videos")):
        self.logs_path = log_path
        self.videos_to_process_path = videos_to_process_path
        self.processed_videos_path = processed_videos_path


    def run_web_server(self):
        web_server_path = os.path.abspath(web_server.__file__)
        subprocess.run(["python", web_server_path])


    def run_video_processor(self):
        video_processor.VideoProcessor(self.logs_path, self.videos_to_process_path, self.processed_videos_path).run()


    def start_threads(self):
        thread.start_new_thread(self.run_web_server)
        thread.start_new_thread(self.run_video_processor)

        log = ""
        while True:
            time.sleep(10)
            start_log_reader = log_reader.GetLog(self.logs_path).run()
            if start_log_reader and log != start_log_reader:
                log = start_log_reader
                print(start_log_reader)

if __name__ == "__main__":
    p = Processor()
    p.start_threads()
