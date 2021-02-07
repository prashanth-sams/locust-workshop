import csv

class CSVReader:

    def __init__(self, fpath):
        self.fpath = fpath
    

    def read_path(self):
        reader = csv.DictReader(open(self.fpath))
        data = []

        for value in reader:
            data.append(value)
        
        return data
