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
            self.field_map[field] = i + 1


    # get all the values as dict[]
    def values(self):
        return self.sheet.get_all_records()

    def find_id(self, id):
        col = self.field_map['id']
        log.debug(f"looking for {id} in col={col}")
        cell = self.sheet.find(str(id), in_column=col) # rampant str() - find() failed for int(id)
        log.debug(f"found row: {cell.row}")
        return cell

    def row(self, id):
        cell = self.find_id(id)
        values = self.sheet.row_values(cell.row)
        # map columns items to names
        row = {}            
        #log.debug(f'{values}')

        for col, value in enumerate(values):
            name = self.fieldnames[col]
            #log.debug(f'{name}')
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
        cell = self.find_id(id)

        # update the values
        for name, value in params.items():
            col = self.field_map[name]
            #log.debug(f"Updating a value: {id}, {name}/{col} -> {value}")

            self.sheet.update_cell(cell.row, col, value)


    def gen_id(self):
        # just get the highest value in 'id' col and add 1.
        col = self.field_map['id']
        vals = self.sheet.col_values(col)
        vals = vals[1:] # strip the 1st value, the header
        return int(max(vals)) + 1

    def add(self, params):
        # generate a new ID
        if 'id' not in params:
            params['id'] = self.gen_id()

        log.debug(f"add:params={params}")

        # create row value list
        row = [None] * (len(self.field_map.items()) + 1)

        for field, value in params.items():
            col = self.field_map.get(field)
            if col:
                row[col] = value
                #log.debug(f"add: {col}/{field} = {params}")
            else:
                log.warn(f'Unknown column name: {field}')

        # the list is too long currently, due to the 1-based index for sheets
        row = row[1:]

        # create a new row
        log.debug(f"Appending row, id={row[0]}: {row}")
        self.sheet.append_row(row)

        return params['id']
