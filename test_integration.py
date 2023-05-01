import discord
import discord.ext.commands as commands
from discord.ext.commands import Cog, command
import pytest
import pytest_asyncio
import discord.ext.test as dpytest

from cogs.tasks import ParamMapper, FileBackingStore, SheetsBackingStore, TaskManager

import random
import datetime

# google sheets
def get_sheets_store():
    try:
        store = SheetsBackingStore("Taskbot Test Sheet")
        return TaskManager(store) # id handling was moved to task manager
    except Exception as ex:
        pytest.skip(f"Cannot load config: {ex}")

def test__sheet_add():
    tasks = get_sheets_store()
    row = {
        'title': f'Test title {random.randint(42, 9999)}',
        'project': random.choice(['acme','rocket','yoyo','skateboard']),
        'status': random.choice(['new','open','working','rejected','closed']),
        'assigned': random.choice(['unassigned','philion','wile','bugs','roadrunner']),
        'updated': datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
    }

    id = tasks.add(row)
    assert id is not None, "id is missing from add() response"

    testrow = tasks.get(id)

    for name, value in row.items():
        assert str(testrow[name]) == str(value)

def test_fieldnames():
    tasks = get_sheets_store()
    assert tasks.fieldnames() == ['id', 'title', 'project', 'status', 'assigned', 'updated', 'notes']

def test_value():
    tasks = get_sheets_store()
    assert tasks.get('4')['project'] == 'yoyo'
    assert tasks.get('1')['assigned'] == 'philion'

def test_sheets_list():
    tasks = get_sheets_store()
    assert tasks.list({'status': 'jolly'})[0]['id'] == 4

def test_sheets_edit():
    tasks = get_sheets_store()

    # confirm status=jolly
    assert tasks.get('4')['status'] == 'jolly'

    # update
    tasks.edit('4', {'status': 'perturbed'})
    assert tasks.get('4')['status'] == 'perturbed'

    # reset to orig
    tasks.edit('4', {'status': 'jolly'})
    assert tasks.get('4')['status'] == 'jolly'
