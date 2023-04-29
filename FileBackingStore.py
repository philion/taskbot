import csv
import logging
from pathlib import Path

log = logging.getLogger(Path(__file__).stem)

class FileBackingStore:
    def __init__(self, filename: str):
        self.filename = filename
        self.fieldnames = self._get_fieldnames()

    # get the column titles, as per csv.DictReader
    def _get_fieldnames(self):
        with open(self.filename) as csvfile:
            return csv.DictReader(csvfile).fieldnames
        
    #def fieldnames(self):
    #    return self.fieldnames

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

    def get(self, id, field):
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
            writer = csv.DictWriter(csvfile, self.fieldnames)
            writer.writerow(params)


    def update(self, id, params):
        # read the file
        rows = self.values()

        # update the values
        for row in rows:
            if row['id'] == id:
                row.update(params)
                break;

        # write the file
        self.write(rows)

        log.debug(f"Updated a value: id={id}, {params}")

    def write(self, rows):
        with open(self.filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(rows)

