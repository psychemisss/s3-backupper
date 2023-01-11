"""
Copyright © psychemisss 2022-2023 - https://github.com/psychemisss
Description: S3 automatic backup tool
Version: 1.1.0
"""

import datetime


class Logger:
    def __init__(self, module: str) -> None:
        self.module = module

    @property
    def timestamp(self) -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def debug(self, message: str) -> None:
        print(f"{self.timestamp} {self.module} \033[37m {message}" + "\033[0m")

    def success(self, message: str) -> None:
        print(f"{self.timestamp} {self.module} \033[32m {message}" + "\033[0m")

    def error(self, message: str) -> None:
        print(f"{self.timestamp} {self.module} \033[31m {message}" + "\033[0m")
