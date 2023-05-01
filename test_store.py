import FileBackingStore
import SheetsBackingStore
import logging
import os
import random
import datetime

import TaskManager as tm

log = logging.getLogger(os.path.basename(__file__))

class TestFileBackingStore:

    def test_fieldnames(self):
        store = FileBackingStore.FileBackingStore("test.csv")
        assert store.fieldnames == ['id', 'title', 'project', 'status', 'assigned', 'updated', 'notes']

    def test_value(self):
        store = FileBackingStore.FileBackingStore("test.csv")
        assert store.get('4', 'project') == 'yoyo'
        assert store.get('1', 'assigned') == 'philion'

    def test_find(self):
        store = FileBackingStore.FileBackingStore("test.csv")

        assert store.find({'status': 'jolly'})[0]['id'] == "4"

    def test_update(self):
        store = FileBackingStore.FileBackingStore("test.csv")

        # confirm status=jolly
        assert store.get('4', 'status') == 'jolly'

        # update
        store.update('4', {'status': 'perturbed'})
        assert store.get('4', 'status') == 'perturbed'

        # reset to orig
        store.update('4', {'status': 'jolly'})
        assert store.get('4', 'status') == 'jolly'

class TestSheetsBackingStore:
        
    def test_add(self):
        store = SheetsBackingStore.SheetsBackingStore("Taskbot Test Sheet")
        tasks = tm.TaskManager(store) # id handling was moved to task manager

        row = {
            'title': f'Test title {random.randint(42, 9999)}',
            'project': random.choice(['acme','rocket','yoyo','skateboard']),
            'status': random.choice(['new','open','working','rejected','closed']),
            'assigned': random.choice(['unassigned','philion','wile','bugs','roadrunner']),
            'updated': datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
        }

        id = tasks.add(row)
        assert id is not None, "id is missing from add() response"

        testrow = store.row(id)
        log.debug(f"{id} - {testrow}")

        for name, value in row.items():
            assert str(testrow[name]) == str(value)

    def test_fieldnames(self):
        store = SheetsBackingStore.SheetsBackingStore("Taskbot Test Sheet")
        assert store.fieldnames == ['id', 'title', 'project', 'status', 'assigned', 'updated', 'notes']

    def test_value(self):
        store = SheetsBackingStore.SheetsBackingStore("Taskbot Test Sheet")
        assert store.get('4', 'project') == 'yoyo'
        assert store.get('1', 'assigned') == 'philion'

    def test_find(self):
        store = SheetsBackingStore.SheetsBackingStore("Taskbot Test Sheet")
        assert store.find({'status': 'jolly'})[0]['id'] == 4

    def test_update(self):
        store = SheetsBackingStore.SheetsBackingStore("Taskbot Test Sheet")

        # confirm status=jolly
        assert store.get('4', 'status') == 'jolly'

        # update
        store.update('4', {'status': 'perturbed'})
        assert store.get('4', 'status') == 'perturbed'

        # reset to orig
        store.update('4', {'status': 'jolly'})
        assert store.get('4', 'status') == 'jolly'
