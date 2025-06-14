import discord
import os, datetime, pytz
from discord.ext import commands, tasks
from discord import app_commands
from discord.ext import commands
from database import ScdbIdols, ScdbSeiyuu

class Birthday(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.idolBirthday.start()
        self.seiyuuBirthday.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded cog 'birthday'")

    def cog_unload(self):
        self.seiyuuBirthday.cancel()
        self.idolBirthday.cancel()

    @tasks.loop(time=datetime.time(hour=0, minute=0, second=0, tzinfo=pytz.timezone('Asia/Tokyo')))
    #@tasks.loop(seconds=10)
    async def idolBirthday(self):
        for idol in ScdbIdols.select().where(ScdbIdols.birthday == datetime.datetime.now(
                pytz.timezone('Asia/Tokyo')).strftime("%m/%d")):
            for cId in os.environ.get("NOTIFY").split(","):
                channel = self.bot.get_channel(int(cId))
                if idol.idol_id == 18:
                    await channel.send("私、" + idol.idol_name + "の誕生日です！\nわあ～♡このプレゼント、すっごく可愛いです～♡")
                else:
                    await channel.send(idol.idol_name + "の誕生日です！")

    @tasks.loop(time=datetime.time(hour=0, minute=0, second=0, tzinfo=pytz.timezone('Asia/Tokyo')))
    #@tasks.loop(seconds=10)
    async def seiyuuBirthday(self):
        for seiyuu in ScdbSeiyuu.select().where(ScdbSeiyuu.seiyuu_birth_date == datetime.datetime.now(
                pytz.timezone('Asia/Tokyo')).strftime("%m/%d")):
            for cId in os.environ.get("NOTIFY").split(","):
                channel = self.bot.get_channel(int(cId))
                if seiyuu.seiyuu_index == 18:
                    await channel.send("今日は" + seiyuu.seiyuu_name + "さんの誕生日です！\nえりちお誕生日おめでとう！")
                else:
                    await channel.send(seiyuu.seiyuu_name + "さんの誕生日です！")

    @app_commands.command(name="seiyuu_birthday", description="查詢今天生日的聲優")
    @app_commands.allowed_installs(users=True, guilds=True)
    async def seiyuu_birthday_search(self, interaction: discord.Interaction):
        await interaction.response.defer()
        flag = False
        for seiyuu in ScdbSeiyuu.select().where(ScdbSeiyuu.seiyuu_birth_date == datetime.datetime.now(
                pytz.timezone('Asia/Tokyo')).strftime("%m/%d")):
            flag = True

            if seiyuu.seiyuu_index == 18:
                await interaction.followup.send("今日は" + seiyuu.seiyuu_name + "さんの誕生日です！\nえりちお誕生日おめでとう！")
            else:
                await interaction.followup.send(seiyuu.seiyuu_name + "さんの誕生日です！")
        if not flag:
            await interaction.followup.send("查無資料!")

    @idolBirthday.before_loop
    @seiyuuBirthday.before_loop
    async def before_birthday(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Birthday(bot))
