#! /usr/bin/env python3
# This example requires the 'message_content' intent.

import discord
import os
import sys

from dotenv import load_dotenv
from ghapi.all import GhApi

# setup client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('list'):
        msg = list_issues()
        await message.channel.send(msg)


def list_issues():
    api = GhApi()
    issues = api.issues.list_for_repo(owner="philion", repo="taskbot")

    response_str = "-"
    for issue in issues:
        response_str = f'{response_str}\n{issue}'

    return response_str


def main(args=None):
    # load the secrets
    load_dotenv()
    discord_token = os.getenv("DISCORD_TOKEN")
    # github_token = os.getenv("GITHUB_TOKEN") #accessed directly in env

    # run the client
    client.run(discord_token)


if __name__ == '__main__':
    rc = 1
    try:
        main()
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
    sys.exit(rc)
