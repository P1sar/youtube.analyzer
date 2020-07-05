import boto3
import logging
import os

from io import BytesIO


BUCKET_FILE_NAME = 'channels.csv'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class S3Client(object):
    def __init__(self, key=None, secret=None, endpoint_url=None):
        self.s3 = boto3.client('s3', endpoint_url=endpoint_url, aws_access_key_id=key, aws_secret_access_key=secret)

    def channels_map(self, bucket_name, filename):
        f = BytesIO()
        self.s3.download_fileobj(bucket_name, filename, f)
        f.seek(0)
        return {line.decode('utf-8').split(",")[-1].strip().split("/")[-1]: line.decode('utf-8').split(",")[0] for line in f.readlines()}

