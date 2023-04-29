#! /usr/bin/env python3
# This example requires the 'message_content' intent.

import discord
import logging
import os
import asyncio

from dotenv import load_dotenv
from github import Github

from discord.ext import commands
from pathlib import Path

# logging
log = logging.getLogger(Path(__file__).stem)

async def main():
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.start('token')


asyncio.run(main())

# setup client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# load the secrets
load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")



# run the client
client.run(discord_token)

class TaskBot(commands.Bot):
    def __init__(self, bot):
        self.bot = bot



class TaskCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    async def list(self, ctx, *, member: discord.Member = None):
        pass

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}~')
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar.')
        self._last_member = member
