#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from datetime import datetime
from log_processor import LogProcessor


class VideoProcessor:
    def __init__(self):
        self.log_processor = LogProcessor()
        self.logs_path = os.path.join(os.getcwd(), "logs")
        self.videos_to_process_path = os.path.join(os.getcwd(), r"videos_to_process")
        self.processed_videos_path = os.path.join(os.getcwd(), r"processed_videos")

    def get_log_info(self):
            logs = os.listdir(self.logs_path)
            if logs:
                last_log_file = self.log_processor.get_last_log(self.logs_path)
                last_log_content = self.log_processor.read_file(last_log_file)
            else:
                last_log_content = ""
            new_log_file_name = "{0}_{1}.txt".format(str(datetime.today()).replace("-", "").split(" ")[0],
                                                     "%.6d" % (len(logs)))
            new_log_file_path = os.path.join(self.logs_path, new_log_file_name)
            return last_log_content, new_log_file_path

    def video_processor(self, path, video_files, new_log_file_path, last_log_content):
        for video in video_files:
            video_file_path = os.path.join(path, video)
            processed_video_path = os.path.join(self.processed_videos_path, os.path.basename(video_file_path))
            ret = requests.post("http://localhost:8080/cut_video",
                                data={"video_path": video_file_path,
                                      "processed_video_path": processed_video_path})
            print(processed_video_path)
            last_log_content += ret.content.decode("utf-8") + "\n"
        self.log_processor.write_log(new_log_file_path, last_log_content)

    def run(self):
        if not os.path.exists(self.processed_videos_path):
            os.mkdir(self.processed_videos_path)
        if not os.path.exists(self.videos_to_process_path):
            os.mkdir(self.videos_to_process_path)
        if not os.path.exists(self.logs_path):
            os.mkdir(self.logs_path)
        while True:
            files_to_process = os.listdir(self.videos_to_process_path)
            if files_to_process:
                last_log_content, new_log_file_path = self.get_log_info()
                self.video_processor(self.videos_to_process_path, files_to_process, new_log_file_path, last_log_content)


if __name__ == "__main__":
    vp = VideoProcessor()
    vp.run()
