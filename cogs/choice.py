import os
from discord import app_commands
from discord.ext import commands
import random

class Choice(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command()
    async def choice(self, ctx) -> None:
        options = ctx.message.content.split(" ")
        if (len(options) <= 1):
            await ctx.send("No options provided.")
            return

        options = options[1:]
        await ctx.send(random.choice(options))

async def setup(bot):
    await bot.add_cog(Choice(bot))
