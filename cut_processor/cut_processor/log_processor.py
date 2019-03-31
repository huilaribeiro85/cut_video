#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class LogProcessor:
    def __init__(self):
        self.all_logs = list()

    def read_file(self, file_path):
        file_open = open(file_path, "r")
        content = file_open.read()
        file_open.close()
        return content

    def write_log(self, file_path, content):
        file_open = open(file_path, "a+")
        content = file_open.write(content)
        file_open.close()
        return content

    def get_last_log(self, log_path):
        log_files = os.listdir(log_path)
        last_log_file_path = None
        last_log_date = None
        for log_file in log_files:
            file_path = os.path.join(log_path, log_file)
            log_date = os.path.getctime(file_path)
            if not last_log_date:
                last_log_date = log_date
            else:
                if last_log_date < log_date:
                    last_log_date = log_date
            last_log_file_path = file_path
        return last_log_file_path
