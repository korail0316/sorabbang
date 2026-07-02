import discord
from discord.ext import commands
from discord import app_commands
import datetime
import re

# 1. 상세 일정 조회 모달
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
                detail = "\n".join([f"• **{e.name}**: {e.start_time.strftime('%p %I:%M')}" for e in events])
                await interaction.followup.send(f"### 📅 {day}일 상세 일정\n{detail}", ephemeral=True)
        except:
            await interaction.followup.send("숫자(일)만 정확히 입력하세요.", ephemeral=True)

# 2. 캘린더 인터페이스
class CalendarView(discord.ui.View):
    def __init__(self, current_date):
        super().__init__(timeout=None)
        self.current_date = current_date

    def get_embed(self, guild):
        target_year, target_month = self.current_date.year, self.current_date.month
        events = [e for e in guild.scheduled_events if e.start_time.astimezone(datetime.timezone.utc).year == target_year and e.start_time.astimezone(datetime.timezone.utc).month == target_month]
        embed = discord.Embed(title=f"📅 {target_year}년 {target_month}월 공용 캘린더", color=discord.Color.teal())
        if not events: embed.description = "등록된 일정이 없습니다."
        else:
            for e in sorted(events, key=lambda x: x.start_time):
                kst = e.start_time + datetime.timedelta(hours=9)
                embed.add_field(name=f"• {kst.day}일: {e.name}", value=f"시간: {kst.strftime('%p %I:%M')}", inline=False)
        return embed

    @discord.ui.button(label="◀ 이전", style=discord.ButtonStyle.secondary)
    async def prev(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_date = (self.current_date.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
        await interaction.response.edit_message(embed=self.get_embed(interaction.guild), view=self)

    @discord.ui.button(label="🔍 상세 확인", style=discord.ButtonStyle.primary)
    async def detail(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DateDetailModal(interaction.guild))

    @discord.ui.button(label="다음 ▶", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_date = (self.current_date.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
        await interaction.response.edit_message(embed=self.get_embed(interaction.guild), view=self)

# 3. 일정 등록 로직
class MemberSelectView(discord.ui.View):
    def __init__(self, data, calendar_msg):
        super().__init__(timeout=60)
        self.data = data
        self.calendar_msg = calendar_msg

    @discord.ui.select(cls=discord.ui.UserSelect, placeholder="함께할 멤버를 선택하세요!", min_values=1, max_values=10)
    async def select_members(self, interaction: discord.Interaction, select: discord.ui.UserSelect):
        await interaction.response.defer(ephemeral=True)
        start_dt = self.data['dt']
        
        # 1. 이벤트 생성
        await interaction.guild.create_scheduled_event(
            name=self.data['name'], 
            start_time=start_dt, 
            end_time=start_dt + datetime.timedelta(hours=1),
            description=self.data['desc'], 
            entity_type=discord.EntityType.external, 
            location="공용 채널", 
            privacy_level=discord.PrivacyLevel.guild_only
        )
        
        # 2. DM 발송 (이 부분이 빠져 있었습니다)
        for user in select.values:
            try: 
                await user.send(f"🔔 **새 일정 알림**: {self.data['name']}\n일시: {start_dt.strftime('%Y-%m-%d %p %I:%M')}\n참여자로 등록되었습니다!")
            except: 
                continue
        
        # 3. 서버 데이터 새로고침
        await interaction.guild.fetch_scheduled_events() 
                
        # [핵심] 캘린더 갱신: original_interaction이 아니라 calendar_msg를 직접 edit
        new_view = CalendarView(datetime.date(self.data['dt'].year, self.data['dt'].month, 1))
        await self.calendar_msg.edit(embed=new_view.get_embed(interaction.guild), view=new_view)
        
        await interaction.followup.send("✅ 캘린더가 즉시 업데이트되었습니다!", ephemeral=True)
class EventModal(discord.ui.Modal, title="새 일정 등록"):
    def __init__(self, original_interaction, calendar_msg):
        super().__init__()
        self.original_interaction = original_interaction
        self.calendar_msg = calendar_msg
    name = discord.ui.TextInput(label="일정 제목")
    date_ymd = discord.ui.TextInput(label="날짜 (YYYY-MM-DD)", placeholder="2026-07-02")
    time_str = discord.ui.TextInput(label="시간 (오전/오후 HH:MM)", placeholder="오후 12:30")
    desc = discord.ui.TextInput(label="상세 내용", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            time_match = re.search(r'(오전|오후)\s*(\d{1,2}):(\d{2})', self.time_str.value)
            ampm, hour, minute = time_match.groups()
            hour = int(hour) + (12 if ampm == '오후' and int(hour) < 12 else 0)
            if ampm == '오전' and hour == 12: hour = 0
            start_dt = datetime.datetime.strptime(self.date_ymd.value, "%Y-%m-%d").replace(hour=hour, minute=int(minute), tzinfo=datetime.timezone.utc)
            data = {'name': self.name.value, 'dt': start_dt, 'desc': self.desc.value}
            await interaction.followup.send("함께할 멤버 선택:", view=MemberSelectView(data, self.calendar_msg), ephemeral=True)
        except: await interaction.followup.send("❌ 시간 형식 오류: '오후 12:30' 처럼 입력해주세요.", ephemeral=True)

class Schedule(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @app_commands.command(name="캘린더생성")
    async def create_calendar(self, interaction: discord.Interaction):
        view = CalendarView(datetime.date.today())
        # 응답을 보내고, 그 응답 메시지 객체를 가져옵니다.
        await interaction.response.send_message(embed=view.get_embed(interaction.guild), view=view)
        # 생성된 메시지를 가져옵니다.
        msg = await interaction.original_response()
        # 이 msg 객체를 일정등록 모달을 열 때 함께 넘겨줘야 합니다.
        self.calendar_message = msg 

    @app_commands.command(name="일정등록")
    async def add_event(self, interaction: discord.Interaction): 
        # 캘린더 메시지가 생성되어 있는지 확인 후 모달 호출
        calendar_msg = getattr(self, 'calendar_message', None)
        await interaction.response.send_modal(EventModal(interaction, calendar_msg))

async def setup(bot): await bot.add_cog(Schedule(bot))
