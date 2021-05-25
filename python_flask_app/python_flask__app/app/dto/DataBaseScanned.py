class DataBaseScanned():
    def __init__(self):
        self.schema_list = []
        
    def add_schemas(self, schema_list):
        buff = []
        for schema in schema_list:
            buff.append(schema.__dict__)

        self.schema_list =  buff
        return self.schema_list