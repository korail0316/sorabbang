import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="일정생성", description="스터디 이벤트를 생성합니다.")
    @app_commands.describe(
        name="일정 제목",
        start_time="시작 시간 (예: 2026-07-05 14:00)",
        description="상세 내용"
    )
    async def create_event(self, interaction: discord.Interaction, name: str, start_time: str, description: str):
        try:
            # 시간 형식 파싱
            start_dt = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
            
            # 이벤트 생성
            await interaction.guild.create_scheduled_event(
                name=name,
                start_time=start_dt,
                description=description,
                entity_type=discord.EntityType.external, # 채널 외의 외부 일정으로 설정
                location="스터디 카페 음성 채널",
                privacy_level=discord.PrivacyLevel.guild_only
            )
            
            await interaction.response.send_message(f"✅ **{name}** 일정이 이벤트로 생성되었습니다!", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("날짜 형식이 잘못되었습니다. `YYYY-MM-DD HH:MM` 형식으로 입력해주세요.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Schedule(bot))
