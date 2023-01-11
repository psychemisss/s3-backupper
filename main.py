"""
Copyright © psychemisss 2022-2023 - https://github.com/psychemisss
Description: S3 automatic backup tool
Version: 1.1.0
"""

import os
import time
from dotenv import load_dotenv
from tools.FileManager import FileManager
from tools.S3Manager import S3Manager
from tools.Logger import Logger
log = Logger(__name__)
load_dotenv()


def main():
    log.success('Starting backup...')
    fm = FileManager(current_path=os.path.realpath(os.path.dirname(__file__)))
    target_directory_path = fm.search_target_dir()
    backup_path, backup_name = fm.create_backup(target_directory_path)

    # TODO: Get configuration using fm.config property

    s3 = S3Manager()
    s3.upload_file(backup_path + ".zip", s3.default_bucket_name, backup_name + ".zip")

    fm.clear_backup(backup_path)
    log.success('Backup finished')


if __name__ == '__main__':
    # launch backup every 5 minutes
    backup_interval = int(os.getenv("BACKUP_INTERVAL")) * 60

    while True:
        main()
        time.sleep(backup_interval)
