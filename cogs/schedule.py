import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="일정생성", description="스터디 이벤트를 생성하여 대표 캘린더에 등록합니다.")
    @app_commands.describe(
        name="일정 제목",
        start_time="시작 시간 (예: 2026-07-05 14:00)",
        description="상세 내용"
    )
    async def create_event(self, interaction: discord.Interaction, name: str, start_time: str, description: str):
        try:
            # 시간 형식 파싱 (현재 연도 2026을 기준으로 함)
            start_dt = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
            
            # 디스코드 서버 이벤트 생성
            event = await interaction.guild.create_scheduled_event(
                name=name,
                start_time=start_dt,
                description=description,
                entity_type=discord.EntityType.external,
                location="스터디 카페 음성 채널",
                privacy_level=discord.PrivacyLevel.guild_only
            )
            
            await interaction.response.send_message(
                f"✅ **{name}** 일정이 성공적으로 생성되었습니다!\n서버 상단 이벤트 탭에서 확인 가능합니다.", 
                ephemeral=True
            )
        except ValueError:
            await interaction.response.send_message(
                "❌ 시간 형식이 잘못되었습니다. `YYYY-MM-DD HH:MM` 형식(예: 2026-07-05 14:00)으로 입력해주세요.", 
                ephemeral=True
            )

    @app_commands.command(name="일정확인", description="서버의 모든 스터디 일정을 모아봅니다.")
    async def view_all_events(self, interaction: discord.Interaction):
        # 현재 서버의 모든 예정된 이벤트 불러오기
        events = interaction.guild.scheduled_events
        
        if not events:
            await interaction.response.send_message("현재 등록된 스터디 일정이 없습니다.", ephemeral=True)
            return

        # 시간을 기준으로 정렬
        sorted_events = sorted(events, key=lambda e: e.start_time)

        embed = discord.Embed(
            title="📅 서버 대표 스터디 캘린더", 
            description="서버에 등록된 예정된 스터디 일정입니다.",
            color=discord.Color.green()
        )
        
        for event in sorted_events:
            start_time = event.start_time.strftime("%m-%d %H:%M")
            embed.add_field(
                name=f"• {event.name}", 
                value=f"시작: {start_time}\n[이벤트 바로가기](https://discord.com/events/{event.guild.id}/{event.id})", 
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Schedule(bot))
