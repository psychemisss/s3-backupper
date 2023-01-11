"""
Copyright © psychemisss 2022-2023 - https://github.com/psychemisss
Description: S3 automatic backup tool
Version: 1.1.0
"""

import boto3
import os
import sys
from dotenv import load_dotenv
from tools.Logger import Logger
log = Logger(__name__)
load_dotenv()


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
            log.success('Bucket found')
        else:
            log.debug('Bucket not found, creating...')
            self.create_bucket()

    def check_bucket(self):
        """Function for checking bucket existence."""
        try:
            bucket_list = self.client.list_buckets()
            log.debug('Bucket list:')
            for bucket in bucket_list["Buckets"]:
                log.debug(f"- {bucket['Name']}")
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
            log.success('Bucket created successfully')
        else:
            log.error('Bucket creation failed, check configuration file.')
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
            log.success(f'Backup "{file_path}" uploaded successfully')
        except Exception as e:
            log.error(f'Backup "{file_path}" upload failed')
            print(e)
