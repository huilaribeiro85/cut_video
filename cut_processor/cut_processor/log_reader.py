#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from cut_processor.cut_processor.log_processor import LogProcessor


class GetLog:
    def __init__(self, log_path):
        self.logs_path = log_path
        self.log_processor = LogProcessor()

    def get_log_info(self):
        logs = os.listdir(self.logs_path)
        if logs:
            last_log_file = self.log_processor.get_last_log(self.logs_path, logs)
            last_log_content = self.log_processor.read_file(last_log_file)
            return last_log_content
        return False

    def run(self):
        if not os.path.exists(self.logs_path):
            os.mkdir(self.logs_path)
        ret = requests.get("http://localhost:8080/log_info").content
        if ret:
            return ret.decode("utf-8")
        return ""

if __name__ == "__main__":
    vp = GetLog()
    log_content = vp.run()
