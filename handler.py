import boto3
import logging
import os

from io import BytesIO


BUCKET_FILE_NAME = 'channels.csv'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run(event, context):
    env_var = os.environ
    logging.info("Lambda started")
    s3 = boto3.client('s3')
    f = BytesIO()
    s3.download_fileobj(env_var["BUCKET_NAME"], BUCKET_FILE_NAME, f)
    f.seek(0)
    for line in f.readlines():
        logging.info(line.decode('utf-8').split(",")[0].strip().split("/")[-1])

