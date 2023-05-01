
import logging
from pathlib import Path

log = logging.getLogger(Path(__file__).stem)

class TaskManager():
    def __init__(self, store):
        self.store = store

    def add(self,  params):
        none_value = params.pop('none', None)
        if none_value:
            # in this case, assume default key 'title'
            params['title'] = none_value
            # TODO there needs to be a general way to handle the tag-less defaults

        if 'id' not in params:
            params['id'] = self.gen_id()

        log.debug(f"params after id: {params}")
        return self.store.add(params)
    
    def gen_id(self):
        # just get the number of records and add 1.
        num_rows = self.store.count()

        log.debug(f"num_rows from store: {num_rows}")

        # note: num_rows contains the length including the header row.
        # -1 to remove header, +1 to add new row
        id = num_rows

        # there's intended flexibility ar
        return id
    
    def edit(self, id, params):
        self.bot.store.update(id, params)
        pass

    def list(self, params):
        log.debug(f"### list {params}")
        return self.bot.store.find(params)
