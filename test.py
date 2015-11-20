# coding:utf-8

import json
import pandas as pd
from pymongo import MongoClient


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


def to_mongo(db, collection, d, host='localhost', port=27017, username=None, password=None):
    """:type d : pd.DataFrame"""
    try:
        db = _connect_mongo(host, port, username, password, db)
        m_collection = db[collection]
        record_json_str = d.to_json(orient='records')
        data = json.loads(record_json_str)
        m_collection.insert(data)
        return True
    except Exception as e:
        return False

if __name__ == '__main__':
    # mongo_host = '192.168.1.91'
    # mongo_port = 20000
    # mongo_db = 'tccdevdb'
    # d = pd.read_csv('static/cfg/LINE01_STN_CFG.csv', encoding='utf-8', dtype=str)
    # to_mongo(mongo_db, 'stn_conf', d, mongo_host, mongo_port)
    # from .data_center.csv.reader import CSVReader
    # CSVReader('01', 'static/cfg/TEMP_PLAN_201407020000_20140702074500.csv', )
    # pass
    from data_center.csv.reader import HeaderCSVReader
    h_csv_reader = HeaderCSVReader('01', 'static/cfg/LINE01_STN_CFG.csv')
    h_csv_reader.to_string()
    h_csv_reader.to_mongodb()






