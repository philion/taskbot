import discord
import discord.ext.commands as commands
from discord.ext.commands import Cog, command
import pytest
import pytest_asyncio
import discord.ext.test as dpytest
import os
import logging

import csvbot

### not ready
#  >       member = guild.members[0]
#test_csvbot.py:37:
#self = SequenceProxy([]), idx = 0

log = logging.getLogger(os.path.basename(__file__))
log.setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)

@pytest_asyncio.fixture
async def bot():
    # DRY somehow with testing class? Bot class?
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    bot = commands.Bot(command_prefix='$', intents=intents)
    # ^build in csvbot, then use here

    dpytest.configure(bot)
    return bot

@pytest_asyncio.fixture(autouse=True)
async def cleanup():
    yield
    await dpytest.empty_queue()

@pytest.mark.asyncio
@pytest.mark.skip(reason="not yet working")
async def test_cols(bot):
    log.debug(bot)

    #guild = bot.guilds[0]
    #member = guild.members[0]
    #channel = guild.text_channels[0]

    await dpytest.message("$cols")

    for expected_col in csvbot.get_cols(csvbot.CSV_FILE):
        assert dpytest.verify().message().contains().content(expected_col)
