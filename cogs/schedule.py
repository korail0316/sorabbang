import discord
from discord.ext import commands
import datetime

# 사용자가 날짜를 입력하면 해당 일정을 보여주는 팝업 모달
class DateDetailModal(discord.ui.Modal, title="날짜 상세 확인"):
    def __init__(self, guild):
        super().__init__()
        self.guild = guild
        
    day_input = discord.ui.TextInput(
        label="확인하고 싶은 날짜 (일)",
        placeholder="예: 05",
        min_length=1,
        max_length=2
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            day = int(self.day_input.value)
            # 해당 날짜의 이벤트 필터링
            events = [e for e in self.guild.scheduled_events if e.start_time.day == day]
            
            if not events:
                await interaction.response.send_message(f"{day}일에는 등록된 일정이 없습니다.", ephemeral=True)
            else:
                detail = "\n".join([f"• **{e.name}**: {e.start_time.strftime('%H:%M')}" for e in events])
                await interaction.response.send_message(f"📅 **{day}일의 일정**\n\n{detail}", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("숫자(일)만 입력해주세요.", ephemeral=True)

# 캘린더 메시지 뷰
class CalendarView(discord.ui.View):
    def __init__(self, current_date):
        super().__init__(timeout=None)
        self.current_date = current_date

    def get_embed(self, guild):
        events = [e for e in guild.scheduled_events if e.start_time.month == self.current_date.month]
        embed = discord.Embed(title=f"📅 {self.current_date.month}월 서버 공용 캘린더", color=discord.Color.teal())
        
        # 간단한 요약 출력
        summary = "\n".join([f"• {e.start_time.day}일: {e.name}" for e in sorted(events, key=lambda x: x.start_time.day)])
        embed.description = summary if summary else "등록된 일정이 없습니다."
        return embed

    @discord.ui.button(label="◀ 이전 달", style=discord.ButtonStyle.secondary)
    async def prev(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_date = (self.current_date.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
        await interaction.response.edit_message(embed=self.get_embed(interaction.guild), view=self)

    @discord.ui.button(label="날짜 클릭하여 상세 확인", style=discord.ButtonStyle.primary)
    async def detail(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DateDetailModal(interaction.guild))

    @discord.ui.button(label="다음 달 ▶", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_date = (self.current_date.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
        await interaction.response.edit_message(embed=self.get_embed(interaction.guild), view=self)

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="캘린더생성")
    @commands.has_permissions(administrator=True)
    async def create_calendar(self, ctx):
        view = CalendarView(datetime.date.today())
        await ctx.send(embed=view.get_embed(ctx.guild), view=view)

async def setup(bot):
    await bot.add_cog(Schedule(bot))
