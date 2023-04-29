import csv
import logging
from pathlib import Path
import gspread

log = logging.getLogger(Path(__file__).stem)

class SheetsBackingStore:
    def __init__(self, name: str):
        gc = gspread.service_account()
        sh = gc.open(name)
        self.sheet = sh.sheet1
        self.fieldnames = self.sheet.row_values(1)
        self.field_map = {}
        # index of fields, and their 1-based sheet index
        for i, field in enumerate(self.fieldnames):
            self.field_map[field] = i

    def _field_idx(self, id):
        return self.field_map[id]

    # get all the values as dict[]
    def values(self):
        return self.sheet.get_all_records()

    def find_id(self, id):
        col = self._field_idx('id')
        log.debug("column for id: {col}")
        cell = self.sheet.find(id, in_column=col)
        log.debug("found row: {cell.row}")
        return cell

    def row(self, id):
        cell = self.find_id(id)
        values = self.sheet.row_values(cell.row)
        # map columns items to names
        row = {}            
        log.debug(f'{values}')

        for col, value in enumerate(values):
            name = self.fieldnames[col]
            log.debug(f'{name}')
            row[name] = value

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

    def update(self, id, params):
        # find a row

        # update the values

        log.debug(f"Updated a value: id={id}, {params}")

    def write(self, rows):
        with open(self.filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(rows)


    def add(self, params):
        with open(self.filename, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, self.fieldnames)
            writer.writerow(params)