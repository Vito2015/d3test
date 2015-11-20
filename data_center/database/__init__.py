# coding:utf-8

from pymongo import MongoClient

from config import mongo_host, mongo_port, mongo_db


def _connect_mongo(host, port, username=None, password=None, db=None):
    """ A util for making a connection to mongodb """
    db = db or 'test'
    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]

db = _connect_mongo(mongo_host, mongo_port, db=mongo_db)
