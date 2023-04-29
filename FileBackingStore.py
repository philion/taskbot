import csv

class FileBackingStore:
    def __init__(self, filename: str):
        self.filename = filename

    # get the column titles, as per csv.DictReader
    def fieldnames(self):
        with open(self.filename) as csvfile:
            return csv.DictReader(csvfile).fieldnames

    # get all the values as dict[]
    def values(self):
        with open(self.filename) as csvfile:
            reader = csv.DictReader(csvfile)
            df = []
            for row in reader:
                df.append(row)

            # TODO return the iterator from the reader? or a seqproxy?
            return df

    def row(self, id):
        # dumb search
        for row in self.values():
            if row['id'] == id:
                return row

    def value(self, id, field):
        found = self.row(id)
        if found:
            return found[field]

    # return any fields that match all suppied params (they are "and"ed)
    def find(self, fields):
        result = []

        # more dumb search
        for row in self.values():
            for key, value in fields.items():
                if row[key] != value:
                    break;
            else: # all values match!
                result.append(row)

        return result


    def add(self, params):
        with open(self.filename, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, self.fieldnames())
            writer.writerow(params)

    def update(self):
        pass