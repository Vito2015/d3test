# coding:utf-8
import pandas as pd
from abc import ABCMeta, abstractmethod
from .import db


class MongodbReader(object, metaclass=ABCMeta):
    def __init__(self):
        self.data_frame = None

    def load_frame(self, collection, *args, **kwargs):
        _collection = db[collection]
        self.data_frame = pd.DataFrame(_collection.find(*args, **kwargs))

    @abstractmethod
    def get_data(self, *args, **kwargs): pass


class HeaderMongodbReader(MongodbReader):
    __collection__ = 'stn_conf'

    def __init__(self):
        super(HeaderMongodbReader, self).__init__()

    def get_data(self, line_no):
        self.load_frame(self.__collection__, {'line_no': line_no})
        header_header = 'trip,type,direction,'
        header_item = 'stop|%s|%s|%d|%d|%s'	 # stop|station name|station id|distance|A or D
        header = header_header
        for index, row in self.data_frame.iterrows:
            header_item1 = header_item % (row['stn_name'], row['stn_id'], row['distance'], row['area'], 'A')
            header_item2 = header_item % (row['stn_name'], row['stn_id'], row['distance'], row['area'], 'D')

            header = header + header_item1 + ','
            header = header + header_item2 + ','

        header = header[0:header.rfind(',')]
        header_list = header.split(',')
        return header_list


class TrainPlanMongodbReader(MongodbReader):
    __collection__ = 'train_plan'

    def __init__(self):
        super(TrainPlanMongodbReader, self).__init__()

    def get_data(self, line_no, date):
        self.load_frame(self.__collection__, )
