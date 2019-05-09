import csv
import json
from operator import itemgetter
import config

HOTELDB_FILE = config.HOTELDB_FILE
COLUMN_NAME = config.COLUMN_NAME

class Hotel_DB:
    def __init__(self):
        self.hotelDB_file = HOTELDB_FILE
        self.hotelDB_column = COLUMN_NAME
    
    def get_room(self, room_type, ordering_type):
        result_list = []
        with open(self.hotelDB_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
            for row in csv_reader:
                if(row[2] == room_type):
                    row[3] = int(row[3])
                    result_list.append(row)
        
        return self.to_json(self.sort_result(result_list, ordering_type))

    def get_city(self, city_name, ordering_type):
        result_list = []
        with open(self.hotelDB_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
            for row in csv_reader:
                if(row[0] == city_name):
                    row[3] = int(row[3])
                    result_list.append(row)

        return self.to_json(self.sort_result(result_list, ordering_type))

    def sort_result(self, result_list, ordering_type):
        if(ordering_type == 'ASC'):
            return sorted(result_list, key = itemgetter(3), reverse = False)
        else:
            return sorted(result_list, key = itemgetter(3), reverse = True)

    def to_json(self, result_list):
        return json.dumps(result_list)
