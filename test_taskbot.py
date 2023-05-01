import discord
import discord.ext.commands as commands
from discord.ext.commands import Cog, command
import pytest
import pytest_asyncio
import discord.ext.test as dpytest
from pathlib import Path
import logging

import taskbot as tb


log = logging.getLogger(Path(__file__).stem)

@pytest_asyncio.fixture
async def bot():
    b = tb.test_bot()
    dpytest.configure(b)
    log.debug(f'configured {b}')
    return b


@pytest.mark.asyncio
@pytest.mark.skip(reason="not yet working")
async def test_list(bot):
    log.debug(f'>>>> test_list {bot}')

    #guild = bot.guilds[0]
    #channel = guild.text_channels[0]

    #if len(guild.members) > 0:
    #    member = guild.members[0]
    #else:
    #    log.warn(f"no members!")

    #log.debug(f"{guild}, {channel}, {member}")

    await dpytest.message("$list")
    assert dpytest.verify().message().contains().content("foobar")
