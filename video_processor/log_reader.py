#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from log_processor import LogProcessor


class GetLog:
    def __init__(self):
        self.logs_path = os.path.join(os.getcwd(), "logs")
        self.log_processor = LogProcessor()

    def get_log_info(self):
        logs = os.listdir(self.logs_path)
        if logs:
            last_log_file = self.log_processor.get_last_log(self.logs_path, logs)
            last_log_content = self.log_processor.read_file(last_log_file)
            return last_log_content
        return False

    def run(self):
        ret = requests.get("http://localhost:8080/log_info").content
        print(ret.decode("utf-8"))
        return ret


if __name__ == "__main__":
    vp = GetLog()
    log_content = vp.run()
