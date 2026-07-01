import discord
from discord.ext import commands
from discord import app_commands
import json

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. 일정 추가 명령어
    @app_commands.command(name="일정추가", description="새로운 공부 일정을 추가합니다.")
    @app_commands.describe(date="날짜 (예: 07-05)", content="일정 내용")
    async def add_schedule(self, interaction: discord.Interaction, date: str, content: str):
        # 여기에 데이터를 저장하는 로직을 나중에 붙일 거예요
        await interaction.response.send_message(f"✅ {date}에 '{content}' 일정이 추가되었습니다!", ephemeral=True)

    # 2. 일정 보기 명령어
    @app_commands.command(name="일정보기", description="현재 등록된 스터디 일정을 확인합니다.")
    async def view_schedule(self, interaction: discord.Interaction):
        # 임베드를 통해 깔끔하게 출력
        embed = discord.Embed(
            title="📅 스터디 카페 일정",
            description="현재 등록된 일정이 없습니다.",
            color=discord.Color.purple()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Schedule(bot))
