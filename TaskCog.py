import ParamMapper as pm
from taskbot import log

import discord
from discord.ext import commands
from tabulate import tabulate


async def setup(bot):
    await bot.add_cog(TaskCog(bot))


class TaskCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fields = bot.store.fieldnames # fixme looks like control coupling
        #self.mapper = pm.ParamMapper()
        log.debug(f"init TaskCog with {self.fields}")

    @commands.command()
    async def add(self, ctx, *, params: pm.ParamMapper()):
        none_value = params.pop('none', None)
        if none_value:
            # in this case, assume default key 'title'
            params['title'] = none_value
            # TODO there needs to be a general way to handle the tag-less defaults

        id = self.bot.store.add(params)
        await ctx.send(f'Added id={id} with {params}')

    @commands.command()
    async def edit(self, ctx, *, member: discord.Member = None):
        pass

    @commands.command()
    #async def list(self, ctx, arg):
    async def list(self, ctx, *, params: pm.ParamMapper() = {}):
        #params = self.mapper.parse(arg) # a string with everything
        log.debug(f"list {params}")

        result = self.bot.store.find(params)

        table = self.render_table(result)
        await ctx.send(table)

    def render_table(self, dataset):
        # TODO table headers and formatting
        return f"```\n{tabulate(dataset)}\n```"