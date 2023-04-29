import FileBackingStore
import logging
import os

log = logging.getLogger(os.path.basename(__file__))

class TestFileBackingStore:

    def test_fieldnames(self):
        store = FileBackingStore.FileBackingStore("test.csv")
        assert store.fieldnames() == ['id', 'title', 'project', 'status', 'assigned', 'updated', 'notes']

    def test_value(self):
        store = FileBackingStore.FileBackingStore("test.csv")
        assert store.value('4', 'project') == 'yoyo'
        assert store.value('1', 'assigned') == 'philion'

    def test_find(self):
        store = FileBackingStore.FileBackingStore("test.csv")

        assert store.find({'status': 'jolly'})[0]['id'] == "4"
