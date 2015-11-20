# coding:utf-8

if __name__ == '__main__':
    # pass

    # mongo_host = '192.168.1.91'
    # mongo_port = 20000
    # mongo_db = 'tccdevdb'
    # d = pd.read_csv('static/cfg/LINE01_STN_CFG.csv', encoding='utf-8', dtype=str)
    # to_mongo(mongo_db, 'stn_conf', d, mongo_host, mongo_port)
    # from .data_center.csv.reader import CSVReader
    # CSVReader('01', 'static/cfg/TEMP_PLAN_201407020000_20140702074500.csv', )

    # from data_center.csv.reader import HeaderCSVReader
    # h_csv_reader = HeaderCSVReader('01', 'static/cfg/LINE01_STN_CFG.csv')
    # h_csv_reader.to_string()
    # h_csv_reader.to_mongodb()
    #
    # from data_center.csv.reader import TrainPlanCSVReader
    # plan_reader = TrainPlanCSVReader('static/cfg/TEMP_PLAN_201407020000_20140702074500.csv')
    # plan_reader.to_mongodb()

    # from data_center.database.reader import HeaderMongodbReader
    # h_mongodb_reader = HeaderMongodbReader()
    # header = h_mongodb_reader.get_data('01')
    # print(header)

    from data_center.database.reader import TrainPlanMongodbReader
    train_reader = TrainPlanMongodbReader()
    train_reader.load_frame('01', '20140702')
    data = train_reader.get_data()
    for d in data:
        print(d)





