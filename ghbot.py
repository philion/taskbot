#! /usr/bin/env python3
# This example requires the 'message_content' intent.

import discord
import os

from dotenv import load_dotenv
from github import Github


# setup client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# load the secrets
load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
github_token = os.getenv("GITHUB_TOKEN")
gh = Github(github_token)


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
    repo = gh.get_repo("philion/taskbot")
    issues = repo.get_issues(state='open')
    response_str = "-"
    for issue in issues:
        response_str = f'{response_str}\n{issue}'

    return response_str


# run the client
client.run(discord_token)
