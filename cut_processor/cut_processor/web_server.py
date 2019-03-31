#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import shutil
import time
from datetime import datetime
from flask import Flask, request
from cut_processor.cut_processor import cut_video as cv
from cut_processor.cut_processor.log_processor import LogProcessor

app = Flask(__name__)


def rename_cut_video(processed_video_path, time_to_start_process):
    file_path, file_extension = os.path.splitext(processed_video_path)
    date_file_name = time_to_start_process.strftime("%Y%m%d_%H%M%S")
    new_file_path = file_path + "_" + date_file_name + file_extension
    return new_file_path


# http://localhost:8080/cut_video
@app.route('/cut_video', methods=["POST"])
def cut_video():
    video_path = request.form.get("video_path")
    time_to_start_process = datetime.now()
    start_process_string = time_to_start_process.strftime("%H:%M:%S")
    processed_video_path = request.form.get("processed_video_path")

    # create new file name
    new_file_path = rename_cut_video(processed_video_path, time_to_start_process)
    # verify video time
    video_time = cv.get_video_size_by_time(video_path)
    if video_time > 30:
        # cut if video_time > 30
        str(cv.cut_video(video_path, output_video=processed_video_path))
        shutil.move(processed_video_path, new_file_path)
        video_time = 30
        os.remove(video_path)
    else:
        # move video if video_time <= 30
        time.sleep(1)
        shutil.move(video_path, new_file_path)
    # create video duration
    if video_time < 10:
        video_duration = "00:00:0{0}".format(int(video_time))
    else:
        video_duration = "00:00:{0}".format(int(video_time))
    end_time = datetime.now().strftime("%H:%M:%S")
    file_info = {"processed_video_path": new_file_path,
                 "proc_init_time": start_process_string + ";0",
                 "proc_end_time": end_time + ";{0}".format(video_time - 1),
                 "video_duration": video_duration}
    return json.dumps(file_info, ensure_ascii=False).encode("utf-8")


# http://localhost:8080/log_info
@app.route('/log_info', methods=["GET"])
def log_info(log=LogProcessor()):
    log_path = os.path.join(os.getcwd(), "logs")
    log_file = log.get_last_log(log_path)
    if log_file:
        log_content = log.read_file(log_file)
        return log_content
    return ""


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
