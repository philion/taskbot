#! /usr/bin/env python3

import discord
import logging
import os
import asyncio

from dotenv import load_dotenv
from github import Github
import FileBackingStore as store

from dotenv import load_dotenv
from discord.ext import commands

from pathlib import Path


# setup logging
discord.utils.setup_logging(level=logging.DEBUG)
log = logging.getLogger(Path(__file__).stem)
#log.setLevel(level=logging.DEBUG)

# TaskBot - encapsulate the discord bot operations
class TaskBot(commands.Bot):
    def __init__(self, store): # fixme add typing
        log.debug(f"init TaskBot with {store.__class__}")

        self.store = store

        # load the secrets
        load_dotenv()

        # setup the bot
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix='$', 
            intents=intents,
            description='acmrckt taskbot',
        )

    # run wrapper adds token
    def run(self):
        log.debug("running")
        super().run(os.getenv("DISCORD_TOKEN"))

    async def on_ready(self):
        # load the extensions
        loadconfig = ["TaskCog"]
        for cog in loadconfig:
            try:
                await self.load_extension(cog)
            except Exception as ex:
                log.warning(f'Couldn\'t load cog {cog}: {ex}')
                
        log.info(f'TaskBot ready, Discord v{discord.__version__}')
        AppInfo = await self.application_info()
        log.info(f'Owner: {AppInfo.owner}')
        
def test_bot():
    return TaskBot(store.FileBackingStore("test.csv")) # test store

def main():
    test_bot().run()

if __name__ == '__main__':
    main()