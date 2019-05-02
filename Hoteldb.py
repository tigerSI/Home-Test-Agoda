import numpy
import pandas

HOTELDB_FILE = './hoteldb.csv'
COLUMN_NAME = ['CITY', 'HOTELID', 'ROOM', 'PRICE']

class HotelDB:
    def __init__(self):
        self.hotelDB_file = HOTELDB_FILE
        self.hotelDB_column = COLUMN_NAME

    def read(self):
        pass
    
    def get_room(self, room_type, ordering_type):
        pass

    def get_city(self, city_name, ordering_type):
        pass

