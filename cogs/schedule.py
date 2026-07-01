import discord
from discord.ext import commands
from discord import app_commands
import datetime

# 1. 날짜 입력 모달 (팝업창)
class DateDetailModal(discord.ui.Modal, title="일정 상세 확인"):
    def __init__(self, guild):
        super().__init__()
        self.guild = guild
        
    day_input = discord.ui.TextInput(
        label="확인할 날짜 (일)",
        placeholder="예: 05",
        min_length=1,
        max_length=2
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            day = int(self.day_input.value)
            # 서버에 등록된 이벤트 중 해당 날짜의 이벤트만 필터링
            events = [e for e in self.guild.scheduled_events if e.start_time.day == day]
            
            if not events:
                await interaction.response.send_message(f"📅 {day}일에는 등록된 일정이 없습니다.", ephemeral=True)
            else:
                detail = "\n".join([f"• **{e.name}**: {e.start_time.strftime('%H:%M')}" for e in events])
                await interaction.response.send_message(f"### 📅 {day}일 상세 일정\n\n{detail}", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ 숫자(일)만 정확히 입력해주세요.", ephemeral=True)

# 2. 캘린더 인터페이스 뷰
class CalendarView(discord.ui.View):
    def __init__(self, current_date):
        super().__init__(timeout=None) # 서버 재시작 후에도 버튼 유지
        self.current_date = current_date

    def get_embed(self, guild):
        # 해당 달의 이벤트만 가져오기
        events = [e for e in guild.scheduled_events if e.start_time.month == self.current_date.month and e.start_time.year == self.current_date.year]
        
        embed = discord.Embed(
            title=f"📅 {self.current_date.year}년 {self.current_date.month}월 서버 공용 캘린더",
            description="전체 일정을 확인하세요. '상세 정보 확인' 버튼을 눌러 날짜별 일정을 조회할 수 있습니다.",
            color=discord.Color.teal()
        )
        
        if not events:
            embed.description = "이번 달에 등록된 일정이 없습니다."
        else:
            for e in sorted(events, key=lambda x: x.start_time):
                embed.add_field(name=f"• {e.start_time.day}일: {e.name}", value=f"시간: {e.start_time.strftime('%H:%M')}", inline=False)
        return embed

    @discord.ui.button(label="◀ 이전 달", style=discord.ButtonStyle.secondary)
    async def prev(self, interaction: discord.Interaction, button: discord.ui.Button):
        year = self.current_date.year if self.current_date.month > 1 else self.current_date.year - 1
        month = self.current_date.month - 1 if self.current_date.month > 1 else 12
        self.current_date = datetime.date(year, month, 1)
        await interaction.response.edit_message(embed=self.get_embed(interaction.guild), view=self)

    @discord.ui.button(label="🔍 날짜 클릭하여 상세 확인", style=discord.ButtonStyle.primary)
    async def detail(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DateDetailModal(interaction.guild))

    @discord.ui.button(label="다음 달 ▶", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        year = self.current_date.year if self.current_date.month < 12 else self.current_date.year + 1
        month = self.current_date.month + 1 if self.current_date.month < 12 else 1
        self.current_date = datetime.date(year, month, 1)
        await interaction.response.edit_message(embed=self.get_embed(interaction.guild), view=self)

# 3. 메인 Cog 클래스
class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="캘린더생성", description="관리자 전용: 공용 캘린더 메시지를 생성합니다.")
    @app_commands.checks.has_permissions(administrator=True)
    async def create_calendar(self, interaction: discord.Interaction):
        view = CalendarView(datetime.date.today())
        await interaction.response.send_message(embed=view.get_embed(interaction.guild), view=view)

    @app_commands.command(name="일정등록", description="서버 공용 일정을 등록합니다.")
    async def add_event(self, interaction: discord.Interaction, name: str, start_time: str, description: str):
        try:
            start_dt = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
            await interaction.guild.create_scheduled_event(
                name=name, start_time=start_dt, description=description,
                entity_type=discord.EntityType.external, location="공용 채널", privacy_level=discord.PrivacyLevel.guild_only
            )
            await interaction.response.send_message("✅ 일정이 성공적으로 등록되었습니다!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ 오류: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Schedule(bot))
