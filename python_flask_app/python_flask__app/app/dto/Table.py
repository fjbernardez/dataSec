import json

class Table():
    def __init__(self, table_name):
        self.table_name = table_name
        self.column_list = []
        
    def add_columns(self, columns):
        buff = []
        for column in columns:
            buff.append(column.__dict__)
        
        self.column_list = buff