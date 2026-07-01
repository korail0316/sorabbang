import discord
from discord.ext import commands
from discord import app_commands
import datetime

# 1. 상세 일정 확인 (모달)
class DateDetailModal(discord.ui.Modal, title="날짜별 상세 일정 확인"):
    def __init__(self, guild):
        super().__init__()
        self.guild = guild
    day_input = discord.ui.TextInput(label="확인할 날짜 (일)", placeholder="예: 05", min_length=1, max_length=2)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            day = int(self.day_input.value)
            events = [e for e in self.guild.scheduled_events if e.start_time.day == day]
            if not events:
                await interaction.response.send_message(f"{day}일에는 일정이 없습니다.", ephemeral=True)
            else:
                detail = "\n".join([f"• **{e.name}**: {e.start_time.strftime('%H:%M')}" for e in events])
                await interaction.response.send_message(f"### 📅 {day}일 상세 일정\n{detail}", ephemeral=True)
        except:
            await interaction.response.send_message("숫자(일)만 입력하세요.", ephemeral=True)

# 2. 캘린더 인터페이스
class CalendarView(discord.ui.View):
    def __init__(self, current_date):
        super().__init__(timeout=None)
        self.current_date = current_date

    def get_embed(self, guild):
        events = [e for e in guild.scheduled_events if e.start_time.month == self.current_date.month and e.start_time.year == self.current_date.year]
        embed = discord.Embed(title=f"📅 {self.current_date.year}년 {self.current_date.month}월 서버 공용 캘린더", color=discord.Color.teal())
        if not events: embed.description = "등록된 일정이 없습니다."
        else:
            for e in sorted(events, key=lambda x: x.start_time):
                embed.add_field(name=f"• {e.start_time.day}일: {e.name}", value=f"시간: {e.start_time.strftime('%H:%M')}", inline=False)
        return embed

    @discord.ui.button(label="◀", style=discord.ButtonStyle.secondary)
    async def prev(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_date = (self.current_date.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
        await interaction.response.edit_message(embed=self.get_embed(interaction.guild), view=self)

    @discord.ui.button(label="상세 정보 확인", style=discord.ButtonStyle.primary)
    async def detail(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DateDetailModal(interaction.guild))

    @discord.ui.button(label="▶", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_date = (self.current_date.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
        await interaction.response.edit_message(embed=self.get_embed(interaction.guild), view=self)

# 3. 멤버 선택 (오류 수정됨)
class MemberSelectView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=60)
        self.data = data

    @discord.ui.select(cls=discord.ui.UserSelect, placeholder="함께할 멤버를 선택하세요!", min_values=1, max_values=10)
    async def select_members(self, interaction: discord.Interaction, select: discord.ui.UserSelect):
        members = ", ".join([user.mention for user in select.values])
        start_dt = datetime.datetime.strptime(f"{self.data['date']} {self.data['time']}", "%Y-%m-%d %H:%M")
        await interaction.guild.create_scheduled_event(
            name=self.data['name'], start_time=start_dt, description=f"멤버: {members}\n내용: {self.data['desc']}",
            entity_type=discord.EntityType.external, location="공용 채널", privacy_level=discord.PrivacyLevel.guild_only
        )
        # 상호작용 실패 방지: 메시지를 수정하거나 완료 알림 전송
        await interaction.response.send_message(f"✅ 일정이 등록되었습니다!", ephemeral=True)

class EventModal(discord.ui.Modal, title="새 일정 등록"):
    name = discord.ui.TextInput(label="일정 제목")
    date_ymd = discord.ui.TextInput(label="날짜 (YYYY-MM-DD)", placeholder="2026-07-05")
    time_hm = discord.ui.TextInput(label="시간 (HH:MM)", placeholder="14:00")
    desc = discord.ui.TextInput(label="상세 내용", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        data = {'name': self.name.value, 'date': self.date_ymd.value, 'time': self.time_hm.value, 'desc': self.desc.value}
        await interaction.response.send_message("멤버를 선택하세요:", view=MemberSelectView(data), ephemeral=True)

class Schedule(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @app_commands.command(name="캘린더생성")
    @app_commands.checks.has_permissions(administrator=True)
    async def create_calendar(self, interaction: discord.Interaction):
        view = CalendarView(datetime.date.today())
        await interaction.response.send_message(embed=view.get_embed(interaction.guild), view=view)
    @app_commands.command(name="일정등록")
    async def add_event(self, interaction: discord.Interaction): await interaction.response.send_modal(EventModal())

async def setup(bot): await bot.add_cog(Schedule(bot))
