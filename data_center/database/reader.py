# coding:utf-8
import pandas as pd
from abc import ABCMeta, abstractmethod
from multiprocessing.dummy import Pool as ThreadPool
from .import db


class MongodbReader(object, metaclass=ABCMeta):
    def __init__(self):
        self.data_frame = None

    def __load_frame__(self, collection, *args, **kwargs):
        _collection = db[collection]
        ret = list(_collection.find(*args, **kwargs))
        self.data_frame = pd.DataFrame(ret, dtype=object)

    @abstractmethod
    def load_frame(self, *args, **kwargs): pass


class HeaderMongodbReader(MongodbReader):
    __collection__ = 'stn_conf'

    def __init__(self):
        super(HeaderMongodbReader, self).__init__()

    def load_frame(self, line_no):
        self.__load_frame__(self.__collection__, {'line_no': line_no})
        self.data_frame = self.data_frame.sort_values('seq', ascending=True)

    def get_header_list(self):
        header_header = 'trip,type,direction,'
        header_item = 'stop|%s|%s|%s|%s|%s'	 # stop|station name|station id|distance|A or D
        header = header_header
        for index, row in self.data_frame.iterrows():
            header_item1 = header_item % (row['stn_name'], row['stn_id'], row['distance'], row['area'], 'A')
            header_item2 = header_item % (row['stn_name'], row['stn_id'], row['distance'], row['area'], 'D')

            header = header + header_item1 + ','
            header = header + header_item2 + ','

        header = header[0:header.rfind(',')]
        header_list = header.split(',')
        return header_list

    def get_ascending_stations(self):
        """Returns [(seq,stn_id), ...]"""
        # data_frame is ordered, ascending
        return self.data_frame.loc[:, ['seq', 'stn_id']].to_records(index=False)


class TrainPlanMongodbReader(MongodbReader):
    __collection__ = 'train_plan'

    def __init__(self):
        self._header_reader = HeaderMongodbReader()
        self.header = []
        self.ordered_stn = []
        super(TrainPlanMongodbReader, self).__init__()

    def load_frame(self, line_no, date):
        """
        :type line_no: str
        :type date: str
        """
        self.__load_frame__(self.__collection__, {'$and': [
            {'line_no': line_no},
            {'date': date}
        ]})
        self._load_header(line_no)

    def _load_header(self, line_no):
        self._header_reader.load_frame(line_no)
        self.header = self._header_reader.get_header_list()
        self.ordered_stn = self._header_reader.get_ascending_stations()

    def get_data(self):
        pool = ThreadPool(4)
        line_trains_records = list()
        line_trains_records.append(self.header)
        trip_groups = self.data_frame.groupby('trip')

        # for trip, train_frame in trip_groups:
        #     record_list = self._gen_row(trip, train_frame)
        #     line_trains_records.append(record_list)

        results = pool.map(self._gen_row, trip_groups)
        pool.close()
        pool.join()
        line_trains_records.extend(results)

        return pd.DataFrame(line_trains_records)

    def _gen_row(self, *args):
        trip, train_frame = args[0]
        # train_frame.iloc(0)[0]['direction']:  get first row's direction column value
        record_list = [trip, 'B', train_frame.iloc(0)[0]['direction']]
        time_list = self._gen_train_times(train_frame, self.ordered_stn)
        record_list.extend(time_list)
        return record_list

    @staticmethod
    def _gen_train_times(train_frame, ordered_stn):
        """:type train_frame: pd.DataFrame
            :type ordered_stn: list
        """
        time_list = []
        stn_col = train_frame['stn_id']

        for _, stn in ordered_stn:
            # find row in train_frame where stn_id == stn
            found_row = train_frame[stn_col == stn]
            if len(found_row) == 1:
                # for index, row in train_frame.iterrows():
                #     if row['stn_id'] == stn:
                #         if row['direction'] == '1':
                #             time_list.extend([row['dep_time'], row['arr_time']])
                #         else:
                #             time_list.extend([row['arr_time'], row['dep_time']])
                found_row = found_row.iloc(0)[0]

                if found_row['direction'] == '1':
                    time_list.extend([found_row['dep_time'], found_row['arr_time']])
                else:
                    time_list.extend([found_row['arr_time'], found_row['dep_time']])
            else:
                time_list.append('-')
                time_list.append('-')

        return time_list
