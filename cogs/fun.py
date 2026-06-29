import discord
from discord.ext import commands
from discord import app_commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="포춘쿠키", description="오늘의 점괘를 확인하세요.")
    async def fortune(self, interaction: discord.Interaction):
        messages = ["노력은 배신하지 않아요!", "오늘은 휴식이 필요해요.", "막 찍어도 정답입니다!"]
        embed = discord.Embed(title="🥠 점괘", description=random.choice(messages), color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))
