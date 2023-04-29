#! /usr/bin/env python3

from typing import Any, Optional, Type
import discord
import os
import logging
import csv
import tabulate 
from discord import app_commands
from discord.ext.commands.help import HelpCommand

from dotenv import load_dotenv
from discord.ext import commands
from tabulate import tabulate

#import FileBackingStore as store
import SheetsBackingStore as store
import ParamMapper

# initial version based on local on-disk csv file that is read for every operation. no cache here!
CSV_FILE = "test.csv" # DELETE

# setup logging
discord.utils.setup_logging(level=logging.DEBUG)
log = logging.getLogger(os.path.basename(__file__))

def main():
    bot = CSVBot("Taskbot Test Sheet")

    @bot.command()
    async def rows(ctx):
        all_rows = bot.store.values()
        table = tabulate(all_rows, headers=bot.store.fieldnames)
        await ctx.send("```\n" + table + "\n```")

    @bot.command()
    async def cols(ctx):
        #df = []
        #for field in bot.store.fieldnames(): # this is to for a list of single-element lists.
        #    df.append([field]) 
        table = tabulate(bot.store.fieldnames)
        await ctx.send("```\n" + table + "\n```")


    # https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html#advanced-converters
    @bot.command()
    async def add(ctx, *, params: ParamMapper(CSV_FILE)):
        bot.store.add(params)
        await ctx.send(f'Added row with {params}')


    # uses the same multi-field style as `add`
    # this time to match records in the 
    @bot.command()
    async def find(ctx, *, params: ParamMapper(CSV_FILE)):
        result = bot.store.find(params)
        table = tabulate(result, headers=bot.store.fieldnames)
        await ctx.send("```\n" + table + "\n```")
    
    # RUN the bot
    bot.run()


class CSVBot(commands.Bot):
    def __init__(self, filename: str):
        log.debug("__init__")
        self.store = store.SheetsBackingStore(filename)

        # load the secrets
        load_dotenv()

        # setup the bot
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='$', intents=intents)
    
    def run(self):
        log.debug("run")
        super().run(os.getenv("DISCORD_TOKEN"))

    
# Handles the "operations" against the CSV file
def get_cols(filename: str):
        with open(filename) as csvfile:
            return csv.DictReader(csvfile).fieldnames

def validate_params(params, expected_fields):
    for key, value in params.items():
        if key in expected_fields:
            print(f"{key}, {value}")
        else:
            print(f"missing key: {key}")


if __name__ == '__main__':
    main()