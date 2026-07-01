import discord
from discord.ext import commands
from discord import app_commands
import datetime

class CalendarView(discord.ui.View):
    def __init__(self, current_date):
        super().__init__(timeout=None)
        self.current_date = current_date

    def get_calendar_embed(self, guild):
        # 해당 달의 이벤트만 필터링
        events = [e for e in guild.scheduled_events if e.start_time.month == self.current_date.month]
        
        embed = discord.Embed(
            title=f"📅 {self.current_date.year}년 {self.current_date.month}월 스터디 일정",
            description="서버의 공식 일정입니다. 참여를 원하시면 이벤트를 클릭하세요.",
            color=discord.Color.blue()
        )
        
        if not events:
            embed.description = "이번 달에 등록된 일정이 없습니다."
        else:
            for event in sorted(events, key=lambda e: e.start_time):
                embed.add_field(name=f"• {event.name}", value=f"일시: {event.start_time.strftime('%d일 %H:%M')}", inline=False)
        return embed

    @discord.ui.button(label="◀ 이전 달", style=discord.ButtonStyle.secondary)
    async def prev_month(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_date = (self.current_date.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
        await interaction.response.edit_message(embed=self.get_calendar_embed(interaction.guild), view=self)

    @discord.ui.button(label="다음 달 ▶", style=discord.ButtonStyle.secondary)
    async def next_month(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_date = (self.current_date.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
        await interaction.response.edit_message(embed=self.get_calendar_embed(interaction.guild), view=self)

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="캘린더생성", description="관리자 전용: 공용 캘린더 메시지를 생성합니다.")
    @app_commands.checks.has_permissions(administrator=True)
    async def create_calendar(self, interaction: discord.Interaction):
        view = CalendarView(datetime.date.today())
        await interaction.response.send_message(embed=view.get_calendar_embed(interaction.guild), view=view)

    @app_commands.command(name="일정생성", description="스터디 이벤트를 생성합니다.")
    async def create_event(self, interaction: discord.Interaction, name: str, start_time: str, description: str):
        try:
            start_dt = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
            await interaction.guild.create_scheduled_event(
                name=name, start_time=start_dt, description=description,
                entity_type=discord.EntityType.external, location="스터디 카페", privacy_level=discord.PrivacyLevel.guild_only
            )
            await interaction.response.send_message("✅ 일정이 추가되었습니다! 캘린더를 확인하세요.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"오류 발생: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Schedule(bot))
