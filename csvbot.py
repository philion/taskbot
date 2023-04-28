#! /usr/bin/env python3
# This example requires the 'message_content' intent.

import discord
import os
import logging
import csv
import re

from dotenv import load_dotenv
from discord.ext import commands
from tabulate import tabulate

# initial version based on local on-disk csv file that is read for every operation. no cache here!
CSV_FILE = "test.csv"

def main():
    # setup logging
    #discord.utils.setup_logging(level=logging.DEBUG)
    #logging.getLogger().setLevel(logging.DEBUG) # for dev
    log = logging.getLogger(os.path.basename(__file__))
    log.setLevel(logging.DEBUG)
    log.info("starting")

    # load the secrets
    load_dotenv()

    # setup the bot
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='$', intents=intents)

    @bot.command()
    async def rows(ctx):
        with open(CSV_FILE) as csvfile:
            reader = csv.DictReader(csvfile)
            df = []
            for row in reader:
                df.append(row.values())
                
            table = tabulate(df, headers=reader.fieldnames)
            await ctx.send("```\n" + table + "\n```")


    @bot.command()
    async def cols(ctx):
        df = []
        for column in get_cols(CSV_FILE):
            df.append([column])
        table = tabulate(df, headers=['column'])
        await ctx.send("```\n" + table + "\n```")


    # https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html#advanced-converters
    @bot.command()
    async def add(ctx, *, params: ParamMapper(CSV_FILE)):
        fields = get_cols(CSV_FILE)
        with open(CSV_FILE, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fields)
            writer.writerow(params)

        await ctx.send(f'Added row with {params}')

    # run the bot
    bot.run(os.getenv("DISCORD_TOKEN"))

    
class ParamMapper(commands.Converter):
    def __init__(self, filename: str):
        self.fields = get_cols(filename)

    def parse(self, param_str):
        params = {}
        last_key = ""
        rest = ""
        for tok in re.split(r'[:=]', param_str):
            try:
                keyi = tok.rindex(' ')
                key = tok[keyi:].strip()
                rest = tok[:keyi].strip()
                #print(f'"{key}", "{rest}"')
            except:
                key = tok.strip()
                # special end condition: no spaces in last segment
                rest = key
                #print(f'{key}')

            # special end condition: last segment has a space, and key has the last segment
            # how can I detect before the split loop break? don't bother, just re-add? but lastkey has been updated.

            if last_key != "" and rest != "":
                params[last_key] = rest
                #print(f'"{last_key}", "{rest}"')
            last_key = key

        # condition breaking split-loop:
        # params contains everything correctly except last_key, which is supposed to be appended to the actual value of the last key.
        params[list(params)[-1]] = tok.strip()

        return params
    
    def validate(self, params):
        for key, value in params.items():
            if key in self.fields:
                print(f"{key}, {value}")
            else:
                print(f"missing key: {key}")


    async def convert(self, ctx, argument):
        params = self.parse(argument)
        #self.validate(params)
        return params

def get_cols(filename: str):
        with open(filename) as csvfile:
            return csv.DictReader(csvfile).fieldnames

if __name__ == '__main__':
    main()