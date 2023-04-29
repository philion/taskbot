import FileBackingStore
import SheetsBackingStore
import logging
import os

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
        store = FileBackingStore.FileBackingStore("test.csv")

        # confirm status=jolly
        assert store.get('4', 'status') == 'jolly'

        # update
        store.update('4', {'status': 'perturbed'})
        assert store.get('4', 'status') == 'perturbed'

        # reset to orig
        store.update('4', {'status': 'jolly'})
        assert store.get('4', 'status') == 'jolly'