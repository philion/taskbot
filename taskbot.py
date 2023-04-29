#! /usr/bin/env python3

import discord
import logging
import os
import asyncio

from dotenv import load_dotenv
from github import Github
import FileBackingStore as store
import ParamMapper as pm

from dotenv import load_dotenv
from discord.ext import commands
from tabulate import tabulate

from pathlib import Path


# setup logging
log = logging.getLogger(Path(__file__).stem)


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
        super().__init__(
            command_prefix='$', 
            intents=intents,
            description='acmrckt taskbot',
        )
    
    async def start(self):
        log.debug("starting")

        # register cogs
        await self.add_cog(TaskCog(self))

        # start
        await super().start(os.getenv("DISCORD_TOKEN"))


# TaskCog - the task-related commands
class TaskCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fields = bot.store.fieldnames
        self.mapper = pm.ParamMapper(self.fields)
        log.debug(f"init TaskCog with {self.fields}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')

    @commands.command()
    async def add(self, ctx, *, member: discord.Member = None):
        pass
    
    @commands.command()
    async def edit(self, ctx, *, member: discord.Member = None):
        pass

    @commands.command()
    async def list(self, ctx, arg = ''):
        params = self.mapper.parse(arg) # a string with everything
        result = self.bot.store.find(params)


        table = tabulate(result, headers=self.fields)
        await ctx.send("```\n" + table + "\n```")
    

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}~')
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar.')
        self._last_member = member


# main()
async def main():
    storage = store.FileBackingStore("test.csv")
    bot = TaskBot(storage)
    async with bot:
        await bot.start()

asyncio.run(main())