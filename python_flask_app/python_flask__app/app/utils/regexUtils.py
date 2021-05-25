import os
import re

class RegexUtils(object):
    def __init__(self):
        work_directory = os.getcwd()
        file_name = work_directory + "\\app\\utils\\information_type.txt"
        self.list_of_type = self.read_types(file_name)

    def read_types(self, file_name):
        reader = open(file_name, "r")
        types = reader.read()
        return types.split("\n")
    
    def get_information_type(self, colum_name):
        colum_name_upper = colum_name.upper()
        for type in self.list_of_type:
            match = re.search(type, colum_name_upper)
            if match is not None:
                return str(type)
        return "N/A"