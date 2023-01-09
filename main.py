import os
import sys
import time
import shutil
import inspect
import datetime
import dataclasses
import boto3


from dotenv import load_dotenv
load_dotenv()


@dataclasses.dataclass
class LogType:
    DEBUG: str = f"DEBUG  \033[37m"
    INFO:  str = f"INFO   \033[32m"
    ERROR: str = f"ERROR  \033[31m"


def log(message: str, status: LogType) -> None:
    frame = inspect.stack()[1]
    frame_info = f"\33[90m {frame.function}():{frame.lineno} \033[0m"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"{timestamp} {status} {message}" + "\033[0m")


# TODO: Move to separate file
class S3Manager:
    def __init__(self, bucket_name: str = os.getenv("S3_BUCKET_NAME")):
        session = boto3.session.Session()
        self.client = session.client(
            service_name='s3',
            endpoint_url=os.getenv("S3_ENDPOINT_URL"),
            aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("S3_SECRET_KEY")
        )
        self.default_bucket_name = bucket_name

        if self.check_bucket():
            log('Bucket found', LogType.INFO)
        else:
            log('Bucket not found, creating...', LogType.DEBUG)
            self.create_bucket()

    def check_bucket(self):
        """Function for checking bucket existence."""
        try:
            bucket_list = self.client.list_buckets()
            log('Bucket list:', LogType.DEBUG)
            for bucket in bucket_list["Buckets"]:
                log(f"- {bucket['Name']}", LogType.DEBUG)
                if bucket["Name"] == os.getenv("S3_BUCKET_NAME"):
                    return True
                else:
                    return False

        except Exception as e:
            print(e)
            return False

    def create_bucket(self):
        """Function for creating a s3 bucket."""
        result = self.client.create_bucket(Bucket=self.default_bucket_name)
        if result["ResponseMetadata"]["HTTPStatusCode"] == 200:
            log('Bucket created successfully', LogType.INFO)
        else:
            log('Bucket creation failed, check configuration file.', LogType.ERROR)
            sys.exit(1)

    def upload_file(self, file_path: str, bucket_name: str, bucket_dir: str = None):
        """
        Function for uploading a file to s3 bucket.

        :param file_path: Path to the file to upload.
        :param bucket_name: Name of the bucket to upload to. If not specified, default bucket name will be used.
        :param bucket_dir: Path to place where file will be uploaded. By default, the bucket is the current date.
        """

        if bucket_dir is None:
            bucket_dir = bucket_name

        try:
            self.client.upload_file(file_path, bucket_name, bucket_dir)
            log(f'Backup "{file_path}" uploaded successfully', LogType.INFO)
        except Exception as e:
            log(f'Backup "{file_path}" upload failed', LogType.ERROR)
            print(e)


# TODO: Move to separate file
class FileManger:
    def __init__(self):
        self.backup_directory = os.getenv("BACKUP_TARGET_DIR")
        self.current_path = os.path.realpath(os.path.dirname(__file__))

    def search_target_dir(self):
        """Function for searching target directory."""
        log(f'Searching "{self.backup_directory}" directory...', LogType.DEBUG)
        for root, directories, files in os.walk(self.current_path):
            for directory in directories:
                if directory == self.backup_directory:
                    target_directory_path = os.path.join(root, directory)
                    log(f'Target directory found: "{target_directory_path}"', LogType.INFO)
                    return target_directory_path

        log('Target directory not found', LogType.ERROR)
        sys.exit(1)

    def create_backup(self, target_directory_path: str):
        """Function for creating a backup of the directory."""
        log('Creating backup...', LogType.DEBUG)
        backup_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        backup_path = os.path.join(self.current_path, backup_name)
        shutil.make_archive(backup_path, "zip", target_directory_path)
        log(f'Backup "{backup_name}.zip" created successfully', LogType.INFO)
        return backup_path, backup_name

    def clear_backup(self, backup_path: str) -> None:
        """Function for clearing zip archives after backup."""
        log('Clearing backup...', LogType.DEBUG)
        os.remove(backup_path + ".zip")

        if os.path.exists(backup_path):
            log('Backup not cleared', LogType.ERROR)
        else:
            log('Backup cleared successfully', LogType.INFO)


def main():
    log('Starting backup...', LogType.INFO)
    file_manager = FileManger()
    target_directory_path = file_manager.search_target_dir()
    backup_path, backup_name = file_manager.create_backup(target_directory_path)

    s3_manager = S3Manager()
    s3_manager.upload_file(backup_path + ".zip", s3_manager.default_bucket_name, backup_name + ".zip")

    file_manager.clear_backup(backup_path)
    log('Backup finished', LogType.INFO)


if __name__ == '__main__':
    # launch backup every 5 minutes
    backup_interval = int(os.getenv("BACKUP_INTERVAL")) * 60

    while True:
        main()
        time.sleep(backup_interval)
