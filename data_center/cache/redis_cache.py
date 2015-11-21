# coding: utf-8
import json
import pandas as pd
from abc import ABCMeta, abstractmethod
from . import redis_client


class RedisCache(object, metaclass=ABCMeta):
    def __init__(self):
        self._data_frame = self._init_data()

    @property
    def data_frame(self):
        # df = self._data_frame
        # """:type df: pd.DataFrame"""
        # records = list()
        # records.append(df.columns)
        # for i, r in df.iterrows():
        #     r[]
        return self._data_frame

    @abstractmethod
    def _init_data(self):
        pass

    @staticmethod
    def set_data(key, value):
        redis_client.set(key, value)

    @staticmethod
    def get_data(key):
        return redis_client.get(key).decode()


class TrainCache(RedisCache):
    def __init__(self, line_no, date, plan_or_real='plan'):
        self._line_no = line_no
        self._date = date
        self._type = plan_or_real.upper() or 'PLAN'
        super(TrainCache, self).__init__()

    def _init_data(self):
        key = 'LINE{}_{}_{}'.format(self._line_no, self._type, self._date)
        json_data = RedisCache.get_data(key)
        data = json.loads(json_data)
        return pd.DataFrame(data)
