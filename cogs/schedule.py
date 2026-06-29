import discord
from discord.ext import commands

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 여기에 캘린더/스케줄 관련 기능을 넣을 예정

async def setup(bot):
    await bot.add_cog(Schedule(bot))
