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

## Initial Prototype - working notes

* Get initial bot working using [discord.py](https://discordpy.readthedocs.io/). DONE
* Adding token management with `.env` file. DONE
* Adding simple github API call to list issues.
* Failure with initial attempt with ghapi. Terrible docs, no example code, cryptic errors. Blah.
* Simple implementation using https://github.com/PyGithub/PyGithub has got list issues working. YAY!
* Demonstrated: Access to both discord and github to access relevant data end-to-end.
