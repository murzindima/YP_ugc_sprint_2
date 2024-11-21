import datetime
import json
import socket

from core.config import app_settings


class Logger:

    map_level = {"ERROR": 1, "INFO": 2, "DEBUG": 3}

    def __init__(self, log_path="app.log", level="INFO"):
        self.log_path = log_path
        self.level = level

    def write_log(self, messages: str, request_id="0", level="INFO"):
        if self.map_level[self.level] >= self.map_level[level]:
            messages["level"] = level
            messages["host"] = socket.gethostname()
            messages["timestamp"] = str(datetime.datetime.now())
            messages["request_id"] = str(request_id)
            messages["app"] = app_settings.app_name
            messages["service"] = app_settings.project_name
            with open(self.log_path, "a") as f:
                json.dump(messages, f)
                f.write("\n")

    def level_update(self, level):
        self.level = level
