# taskbot
A Discord taskbot to mange tasks in a variety of backing stores.

Status: This is a "working proof of concept", not ready-for-production.

## config

`taskbot` configuration is stores in `$HOME/.config/taskbot/config.json`. This seperates the working code (which is regularly checked in) from the sensitive configuration code which usually contains secret keys (and too ofter gets uploaded to github).

That file looks like:
```
{
  "prefix": "$",
  "token": "DISCORD TOKEN",
  "permissions": "YOUR_BOT_PERMISSIONS_HERE",
  "application_id": "YOUR_APPLICATION_ID_HERE",
}
```
and has the following fields:
* `prefix`: character prefix for taskbot commands
* `token` : the Discord token. See [discord.py docs](https://discordpy.readthedocs.io/en/stable/discord.html) to setup a Discord developer token.
* `permissions` : YOUR_BOT_PERMISSIONS
* `application_id` : YOUR_APPLICATION_ID
* `sheets_id` : *optional* The ID of the Google sheet to load. 

See [gspread auth docs](https://docs.gspread.org/en/latest/oauth2.html) on setting up the Google access key.

## running

Once config is done, `make` is used for everthing else:

* `make test` - run the unit tests
* `make integration` - run the integration tests
* `make run` - run the bot locally
* `make venv` - run pip install to build the python environment
* `make clean` - remove all logging, unneeded files, etc.

## deployment

(working notes for current deployment, 05/26)

Plan:
1. Clone to deployment host (`git clone https://github.com/philion/taskbot`)
2. Add config file with secrets (as per **`config`** above)
3. (optional) Add watchdog/autostart to deployment host. Just run in BG for now.
4. Invite bot to CSN discord (https://discordpy.readthedocs.io/en/stable/discord.html#inviting-your-bot)
5. Verify (working on test server)
6. Send announcement.

## v0.4 (future)
TODO: Create an `OSTicketManager` class to integrate directly with OSTicket.

Currently, the design is one-bot-one-backing-store, but that could be backing-store-per-channel.

TODO: Add notification mechanism that runs periodically to return async notification of state changes in the ticket system.

## v0.3 (current)
* Update config to load a specific google sheet by ID. - DONE
* Limit reporting to id, title, assigned. - DONE
* Limit report to 10 (to save chars) SKIP: Fancy tables were getting in the way of readable results. Start simple.
* Test `find`. - Hacky work around for lack of Google API. Handles general match.
* Add link (href, on the ID field) to sheet page? based on response length

## v0.2
Got the new testable framework ported over and running. `make test` is your friend.

Added link to discord.py setup, clean up config initialization details for new config location.
Moved config to ~/.config/taskbot/config.json, keep away from checkins.
Refactored config handling and logging.
Separated unit tests from integration.

Wrote TaskManager based directly on GitHub Issues, and keep running onto client mapping and vlaidation issues. I can't get enough debug logs to firgure out what's failing, and haven't been able to tuen off the screens full of HTTPS trace logs. Time for a big break.

## v0.1
The prototype is working, now to add the bones: simple commands for adding, editing and checking on open tickets. First step is simple use cases.

* list open issues, scoped by forum, with param for project, user, etc. list #project, list @user
* status - status report of # open issues and 
* add -
* update - 

## proof-of-concept - csvbot
A bot backed by simple CSV file, where info can be queried, added and updated.
Eventually, backed by a google sheet.

The bot uses the column names for query and response. i.e. given the columns:

    id, title, project, status, assigned, updated, notes

> $add title="This is a new item" project=ldap
> $update id=23 assigned=Paul
> $find status=open assigned=Paul

That's first pass. Starting with https://interactions-py.github.io/interactions.py/Guides/01%20Getting%20Started/#__tabbed_1_2

Putting the new test bot in `cvsbot.py`.

Working so for, up to adding new rows and listing.

Next up: id mgt and update command and search/select.

csvbot looks pretty good, and can be backed by either FileBackingStore (use a CSV file on local disk) or SheetsBackingStore (use a specific)

test sheet:
https://docs.google.com/spreadsheets/d/1NcwrsdE5YvQAgi9CRLC1Kv69DoIAPQiXlA22MvKzXBo/edit

cli tool to manage csv with SQL: https://mithrandie.github.io/csvq/reference/command.html


## Initial Prototype

* Get initial bot working using [discord.py](https://discordpy.readthedocs.io/). DONE
* Adding token management with `.env` file. DONE
* Adding simple github API call to list issues.
* Failure with initial attempt with ghapi. Terrible docs, no example code, cryptic errors. Blah.
* Simple implementation using https://github.com/PyGithub/PyGithub has got list issues working. YAY!
* Demonstrated: Access to both discord and github to access relevant data end-to-end.

## Design
Thinking about layers of abstractions and contracts. https://en.wikipedia.org/wiki/Design_by_contract

Original plan was "simple CLI tool to manage tasks that worked as bot". This offers a clear directive "simple CLI tool to manage tasks" and can inform a contract for "task manager".

The `TaskManager` can be implemented with Github directly (IssuesStore), or with one of the CSV stores.

Some sample commands:

    taskbot add task with an attribute priority=12
    Added task 53: add task with an attribute

    taskbot edit 53 assign=philion
    Updates task 53: assign=philion

    taskbot list assign=none


python Protocol sample, https://docs.python.org/3/library/typing.html#typing.Protocol https://peps.python.org/pep-0544/
```
from typing import Any, List, Protocol

class Bar(Protocol):
    def oogle(self, quz: List[int]) -> Any:
       ...

def foo(bar: Bar):
    nums = [i for i in range(10)]
    result = bar.oogle(nums)
    return result
```

TODO: Need build-in handling for 'priority' and some sort of mapping?

### Task Manager research
What other "open source task managment cli" tools are there? How do they manage tasks?

google, bing, github, gitlab - start in reverse
nada at gitlab. doesn't seem a good way to find projects

(process involved queries against the above sites, looking for open source projects or articles about "command line task management", diving down for each option unitl I find a user guide that has clear CLI examples. When I find, log here for review later. if not easy to find, like in the readme or top-level docs, move on)

* https://tasklite.org/usage/cli.html (146, haskall)
* https://taskwarrior.org/docs/30second/
* https://ultralist.io/docs/basics/concepts/
* https://github.com/foobuzz/todo/blob/master/doc/guide.md (378, python)
* https://github.com/todotxt/todo.txt-cli/blob/master/USAGE.md (5.2k, sh)
* https://todoman.readthedocs.io/en/stable/man.html
* https://github.com/agateau/yokadi
* https://sambrin.medium.com/fin-command-line-todo-list-made-with-30a2346de068#.naet2hvu4
* https://github.com/mohamed-aziz/mytodo (old)
* https://github.com/boyska/ikog/blob/master/ikog.py (old)

Also handy for research https://tasklite.org/related.html:
* https://github.com/ZeroX-DG/CommitTasks (295)
* https://github.com/naggie/dstask (704, go)
* https://github.com/im-n1/eagle (archived)
* https://github.com/sjl/t (717, python)
* https://dagraham.github.io/etm-dgraham/#reminders (36, python)

that's plenty of options. now a survey of add task, find task, update task, and query for many of the above (again, low hanging fruit)

#### add task
```
tl add Buy milk +groceries
tl add Go running
task add Read Taskwarrior documents later
task add priority:H Pay bills
ultralist add some important task for the +project due tom
ultralist add chat with @bob about +specialProject due:tom
todo add "Do the thing"
todo add "Buy the gift for Stefany" --deadline 2016-02-25
todo add "Backup family pics on my external hard drive" --depends-on 1
todo add "Fix the window" -p 3    # -p is priority
todo add "Read the article about chemistry" -c culture   # note -c is 'context'
todo.sh add "THING I NEED TO DO +project @context"
```

#### find/get task
```
tl info 01e0k6a1p00002zgzc0845vayw
todo task 1
```

#### update task
```
tl do - mark as complete
tl due - set due date
tl boost - increase priority
tl prioritize
tl tag - add a tag
task 2 done - mark task done
task 1 delete
ultralist c 1 - mark task 1 complete
ultralist e 3 chat with @bob
ultralist e 3 due:tom - due tomorrow, not assigned @tom
ultralist e 3 due:none - to remove field
ultralist addnote 1 here is a note - append note to id=1
ultralist ar 1 - archive task 1
ultralist delete 35
ultralist d 35
todo done 1
todo task 2 -p 2
todo edit 1
todo ctx culture --visibility hidden # hide all items in a context
todo ctx culture -p 10 # set all items in context to ptiority 10
todo.sh append ITEM# "TEXT TO APPEND"
todo.sh do ITEM# # mark done
```

#### query
```
tl - list of id, pri, opened, body
tl head
tl all
tl open - all open
tl find
task - same as task next
task next - list based on priority
ultralist list
ultralist l completed:true
ultralist l completed:tod
todo # list all
todo.sh list
todo.sh listall
```

## Notes
https://github.com/Rapptz/discord.py seems the best client lib for Python.
https://github.com/interactions-py/interactions.py looks like an insteresting alternative. - meh. poor docs.

Noting CSV import function of https://tasklite.org

### Work Log

Just noticed the way I was weaving this doc together, I wasn't leaving myself very clear notes.

Underlying bot is working with existing (feature-incomplete) expectations. Next step is "update" function, which will require managing the file contents for a full file re-write (the only option, I think, unless the CSV libs provide one). Simple testing in place to keep me from tracking down syntax error via the full discord bot deployment, but dpytest isn't working yet.

----

I've gotten add and list working in taskbot, and testing has been tedious, so it's once again time to poke on dpytest and test without the discord client. Perhaps it will be good to walk thru the debugger to get that working end-to-end.

Still no dpytest love. The sample tests work, but the special async hooks that are making taksbot run for real are getting in the way.

Time to implement the TaskManager Protocol and test against that.

Got that async hook working with taskbot, after a complete refactor and adding the correct intents! But it's still not reliable as I test.

Back to TaskManager and hand testing in discord client.

TaskCog/taskbot is working with dpytest, running inside a standard discord bot template. Will port everything over to that project in daylight.

Once ported (readme, tests, other code), github actions for standard build would be nice (make report generates report to?)

Rough sketch:
- Get update() and a few more tests working - DONE
- Add google sheet backing - DONE, except for add() - DONE!
- SheetBacking add() and supporting test case. - DONE!
- Research and recommend taskbot command, generate TaskManager UX and contract
- Add task bot commands! - list and add working
- Figure out cogs in discord.py - DONE! TaskCog running
- get dpytest running - DONE
- port template-based bot solution back to taskbot, call it v0.2. - DONE
- tasksh - get a simple shell running to eval commands, and capture inputs for testing.
- github actions to run build on master checking, generate a good profile and coverage report using pytest
- think about: discord wrapper for any of the Task Manager project. really just a question of backing store.
- generic discord wrapper for any CLI?
- containerize the bot
- pytest reports, and how are they stored in GH actions? See: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python
- better formatting on the results, length<2000, cols to display, etc.
- separate unit from intergration tests.
