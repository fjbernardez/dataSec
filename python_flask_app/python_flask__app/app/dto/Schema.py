import json
from app.dto import Table

class Schema():
    def __init__(self, schema_name):
        self.schema_name = schema_name
        self.table_list = []
    
    def add_tables(self, tables):
        buff = []
        for table in tables:
            buff.append(table.__dict__)
        self.table_list = buff
