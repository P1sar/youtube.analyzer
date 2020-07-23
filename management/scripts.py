import sys
sys.path = ['', '..'] + sys.path[1:]

import os
import config as my_config

from sqlalchemy.orm import load_only, sessionmaker
from postgres.models import Channel, AccountKey
from sqlalchemy import create_engine
from s3 import S3Client


def propagate_db_with_channels_from_s3():
    s3_provider = S3Client(key="minio-key", secret="minio-secret", endpoint_url="http://localhost:9000")
    channels_map = s3_provider.channels_map(os.environ.get("BUCKET_NAME", "channels"), os.environ.get("CHANNELS_FILENAME", "channels.csv"))

    engine = create_engine(my_config.DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    existed_channels = session.query(Channel).options(load_only("id")).all()
    ids = [c.id for c in existed_channels]

    channels_to_add = []
    for channel_id in channels_map:
        if channel_id not in ids:
            c = Channel(id=channel_id, name=channels_map[channel_id])
            channels_to_add.append(c)

    session.bulk_save_objects(channels_to_add)
    session.commit()


propagate_db_with_channels_from_s3()


def propagate_db_with_api_keys():
    s3_provider = S3Client(key="minio-key", secret="minio-secret", endpoint_url="http://localhost:9000")
    keys_arr = s3_provider.keys_array(os.environ.get("BUCKET_NAME", "channels"), os.environ.get("CHANNELS_FILENAME", "apiKeys.txt"))

    engine = create_engine(my_config.DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    existedKyes = [k.key for k in session.query(AccountKey).all()]
    account_keys = [AccountKey(key=k.decode('UTF-8').replace("\r\n", "")) for k in list(filter(lambda k: k.decode('UTF-8').replace("\r\n", "") not in existedKyes, keys_arr))]
    print("Keys to add {}".format(len(account_keys)))
    session.bulk_save_objects(account_keys)
    session.commit()


propagate_db_with_api_keys()