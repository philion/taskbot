import discord
import discord.ext.commands as commands
from discord.ext.commands import Cog, command
import pytest
import pytest_asyncio
import discord.ext.test as dpytest

from cogs.tasks import ParamMapper, FileBackingStore, SheetsBackingStore, TaskManager, GitHubIssueManager

import random
import datetime
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logging.getLogger("github.Requester:Requester.py").setLevel(logging.INFO)

# github issues
@pytest.fixture
def gh_tasks():
    try:
        return GitHubIssueManager()
    except Exception as ex:
        pytest.skip(f"Cannot load config: {ex}")

@pytest.mark.skip
def test_gh_add(gh_tasks):
    issue = {
        'title': f'Test issue {random.randint(42, 9999)}',
        'label': random.choice(['acme','rocket','yoyo','skateboard']),
        'state': random.choice(['new','open','working','rejected','closed']),
        'assignee': random.choice(['unassigned','philion','wile','bugs','roadrunner']),
    }

    id = gh_tasks.add(issue)
    assert id is not None, "id is missing from add() response"

    check = gh_tasks.get(id)

    log.debug(f"add check = {check}")

    for name, value in issue.items():
        assert str(check[name]) == str(value)

@pytest.mark.skip
def test_gh_list(gh_tasks):
    resp = gh_tasks.list({'status': 'jolly'})
    log.debug(f"list resp = {resp}")
    #assert [0]['id'] == 4


# google sheets
@pytest.fixture
def tasks():
    try:
        store = SheetsBackingStore("Taskbot Test Sheet")
        return TaskManager(store) # id handling was moved to task manager
    except Exception as ex:
        pytest.skip(f"Cannot load config: {ex}")

def test_add(tasks):
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

def test_list(tasks):
    assert tasks.list({'status': 'jolly'})[0]['id'] == 4

def test_fieldnames(tasks):
    assert tasks.fieldnames() == ['id', 'title', 'project', 'status', 'assigned', 'updated', 'notes']

def test_value(tasks):
    assert tasks.get('4')['project'] == 'yoyo'
    assert tasks.get('1')['assigned'] == 'philion'

def test_sheets_list(tasks):
    assert tasks.list({'status': 'jolly'})[0]['id'] == 4

def test_sheets_edit(tasks):
    # confirm status=jolly
    assert tasks.get('4')['status'] == 'jolly'

    # update
    tasks.edit('4', {'status': 'perturbed'})
    assert tasks.get('4')['status'] == 'perturbed'

    # reset to orig
    tasks.edit('4', {'status': 'jolly'})
    assert tasks.get('4')['status'] == 'jolly'
