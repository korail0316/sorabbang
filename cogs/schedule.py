import discord
from discord.ext import commands
from discord import app_commands
import datetime
import re

# 1. 상세 일정 조회 모달 (기존 유지)
class DateDetailModal(discord.ui.Modal, title="날짜별 상세 일정 확인"):
    def __init__(self, guild):
        super().__init__()
        self.guild = guild
    day_input = discord.ui.TextInput(label="확인할 날짜 (일)", placeholder="예: 05", min_length=1, max_length=2)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            day = int(self.day_input.value)
            events = [e for e in self.guild.scheduled_events if e.start_time.day == day]
            if not events:
                await interaction.followup.send(f"📅 {day}일에는 일정이 없습니다.", ephemeral=True)
            else:
                detail = "\n".join([f"• **{e.name}**: {e.start_time.strftime('%H:%M')}" for e in events])
                await interaction.followup.send(f"### 📅 {day}일 상세 일정\n{detail}", ephemeral=True)
        except:
            await interaction.followup.send("숫자(일)만 입력하세요.", ephemeral=True)

# 2. 캘린더 보기 뷰 (기존 유지)
class CalendarView(discord.ui.View):
    def __init__(self, current_date):
        super().__init__(timeout=None)
        self.current_date = current_date

    def get_embed(self, guild):
        events = [e for e in guild.scheduled_events if e.start_time.month == self.current_date.month and e.start_time.year == self.current_date.year]
        embed = discord.Embed(title=f"📅 {self.current_date.year}년 {self.current_date.month}월 공용 캘린더", color=discord.Color.teal())
        if not events: embed.description = "등록된 일정이 없습니다."
        else:
            for e in sorted(events, key=lambda x: x.start_time):
                embed.add_field(name=f"• {e.start_time.day}일: {e.name}", value=f"시간: {e.start_time.strftime('%p %I:%M')}", inline=False)
        return embed

    @discord.ui.button(label="◀ 이전", style=discord.ButtonStyle.secondary)
    async def prev(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_date = (self.current_date.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
        await interaction.response.edit_message(embed=self.get_embed(interaction.guild), view=self)

    @discord.ui.button(label="🔍 상세 정보 확인", style=discord.ButtonStyle.primary)
    async def detail(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DateDetailModal(interaction.guild))

    @discord.ui.button(label="다음 ▶", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_date = (self.current_date.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
        await interaction.response.edit_message(embed=self.get_embed(interaction.guild), view=self)

# 3. 일정 등록 및 멤버 선택 (시간대 오류 수정 완료)
class MemberSelectView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=60)
        self.data = data

    @discord.ui.select(cls=discord.ui.UserSelect, placeholder="함께할 멤버를 선택하세요!", min_values=1, max_values=10)
    async def select_members(self, interaction: discord.Interaction, select: discord.ui.UserSelect):
        await interaction.response.defer(ephemeral=True)
        
        start_dt = self.data['dt']
        # external 이벤트는 end_time이 필수 (시작 시간 + 1시간으로 설정)
        end_dt = start_dt + datetime.timedelta(hours=1)
        
        try:
            await interaction.guild.create_scheduled_event(
                name=self.data['name'], 
                start_time=start_dt, 
                end_time=end_dt,  # 종료 시간 설정 추가
                description=self.data['desc'],
                entity_type=discord.EntityType.external, 
                location="공용 채널", 
                privacy_level=discord.PrivacyLevel.guild_only
            )
            for user in select.values:
                try: await user.send(f"🔔 **일정 알림**: {self.data['name']} ({start_dt.strftime('%Y-%m-%d %p %I:%M')})")
                except: continue
            await interaction.followup.send("✅ 일정이 등록되고 알림이 발송되었습니다!", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ 이벤트 생성 실패: {e}", ephemeral=True)

class EventModal(discord.ui.Modal, title="새 일정 등록"):
    name = discord.ui.TextInput(label="일정 제목")
    date_ymd = discord.ui.TextInput(label="날짜 (YYYY-MM-DD)", placeholder="2026-07-02")
    time_str = discord.ui.TextInput(label="시간 (오전/오후 HH:MM)", placeholder="오후 12:30")
    desc = discord.ui.TextInput(label="상세 내용", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            time_match = re.search(r'(오전|오후)\s*(\d{1,2}):(\d{2})', self.time_str.value)
            ampm, hour, minute = time_match.groups()
            hour = int(hour)
            if ampm == '오후' and hour < 12: hour += 12
            if ampm == '오전' and hour == 12: hour = 0
            
            naive_dt = datetime.datetime.strptime(self.date_ymd.value, "%Y-%m-%d").replace(hour=hour, minute=int(minute))
            start_dt = naive_dt.replace(tzinfo=datetime.timezone.utc)
            
            data = {'name': self.name.value, 'dt': start_dt, 'desc': self.desc.value}
            await interaction.followup.send("함께할 멤버를 선택하세요:", view=MemberSelectView(data), ephemeral=True)
        except: await interaction.followup.send("❌ 시간 형식 오류: '오후 12:30' 처럼 입력해주세요.", ephemeral=True)

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
