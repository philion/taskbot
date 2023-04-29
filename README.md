# taskbot
A Discord taskbot that uses GitHub tasks as a backing store.

## config

**`.env`** - Contains secrets loaded from an ENV file. Requires `DISCORD_TOKEN` set with a valid Discord app token:

    DISCORD_TOKEN=discord-token
    GITHUB_TOKEN=your-github-token


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

## Initial Prototype - working notes

* Get initial bot working using [discord.py](https://discordpy.readthedocs.io/). DONE
* Adding token management with `.env` file. DONE
* Adding simple github API call to list issues.
* Failure with initial attempt with ghapi. Terrible docs, no example code, cryptic errors. Blah.
* Simple implementation using https://github.com/PyGithub/PyGithub has got list issues working. YAY!
* Demonstrated: Access to both discord and github to access relevant data end-to-end.

## Notes
https://github.com/Rapptz/discord.py seems the best client lib for Python.
https://github.com/interactions-py/interactions.py looks like an insteresting alternative.