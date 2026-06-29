import discord
from discord.ext import commands
from discord import app_commands

# 1. 유저 선택 메뉴를 위한 클래스 별도 정의
class MemberSelect(discord.ui.UserSelect):
    def __init__(self):
        super().__init__(placeholder="함께 공부할 멤버를 선택하세요!", min_values=1, max_values=5)

    async def callback(self, interaction: discord.Interaction):
        user_names = ", ".join([user.mention for user in self.values])
        await interaction.response.send_message(f"공부 메이트: {user_names}\n타이머를 시작합니다! 50분 동안 집중하세요!", ephemeral=False)

# 2. View 클래스에 위에서 만든 Select를 추가
class StudyTimerView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(MemberSelect())

# 3. Cog 클래스
class Study(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="타이머", description="공부 메이트와 함께하는 집중 타이머")
    async def timer(self, interaction: discord.Interaction):
        view = StudyTimerView()
        await interaction.response.send_message("누구와 함께 공부하시겠어요?", view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Study(bot))
