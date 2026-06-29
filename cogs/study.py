import discord
from discord.ext import commands
from discord import app_commands

# 1. 시간 입력 모달 (타이머 시작 알림)
class TimeInputModal(discord.ui.Modal, title='시간 설정'):
    minutes = discord.ui.TextInput(label='공부할 시간(분)', placeholder='예: 50', min_length=1, max_length=3)

    def __init__(self, selected_users):
        super().__init__()
        self.selected_users = selected_users

    async def on_submit(self, interaction: discord.Interaction):
        time_val = self.minutes.value
        user_names = ", ".join([user.mention for user in self.selected_users])
        
        # 큰 숫자를 표출하기 위해 # 헤더 마크다운 사용
        embed = discord.Embed(
            title="⏱️ 타이머 시작",
            description=f"**멤버:** {user_names}\n\n## {time_val}분 동안 타이머가 설정 되었습니다.",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=False)

# 2. 멤버 선택 UI (임베드 포함)
class MemberSelect(discord.ui.UserSelect):
    def __init__(self):
        super().__init__(placeholder="멤버 선택...", min_values=1, max_values=5)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TimeInputModal(self.values))

class StudyTimerView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(MemberSelect())

class Study(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="타이머", description="멤버와 함께하는 집중 타이머")
    async def timer(self, interaction: discord.Interaction):
        # 임베드 안에 멤버 선택 메뉴를 넣어 깔끔하게 표출
        embed = discord.Embed(
            title="📚 스터디 세션 설정",
            description="아래 메뉴에서 **함께 공부할 멤버를 선택**해 주세요.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, view=StudyTimerView(), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Study(bot))
