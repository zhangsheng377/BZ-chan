import os

from UTILS.cache_redis import CacheRedis
from UTILS.database_factory import DatabaseFactory

MONGODB_HOST = os.getenv('MONGODB_HOST')
MONGODB_PORT = int(os.getenv('MONGODB_PORT'))
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))


def get_db_sheet(database_name, sheet_name):
    database_factory = DatabaseFactory(host=MONGODB_HOST, port=MONGODB_PORT, model='pymongo')
    return database_factory.get(database_name=database_name, sheet_name=sheet_name)


cache_redis = CacheRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def get_db_bz_chans():
    db_sheet = get_db_sheet(database_name="bz_chan", sheet_name="bz_chan")
    return db_sheet.find()


def get_bz_chans():
    return cache_redis.get_cache_from_db('bz_chans', get_db_bz_chans)


def get_bz_chan(send_key):
    bz_chans = get_bz_chans()
    for bz_chan in bz_chans:
        if send_key == bz_chan['_id']:
            return bz_chan
    return None
