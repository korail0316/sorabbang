import discord
from discord.ext import commands
from discord import app_commands

class StudyTimerView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.user_select(placeholder="함께 공부할 멤버를 선택하세요!", min_values=1, max_values=5)
    async def select_members(self, interaction: discord.Interaction, select: discord.ui.UserSelect):
        selected_users = select.values
        user_names = ", ".join([user.mention for user in selected_users])
        
        await interaction.response.send_message(f"멤버: {user_names}\n타이머를 시작합니다! 50분 동안 집중하세요!", ephemeral=False)
        # 여기에 추후 타이머 로직(비동기 sleep 등)을 추가할 예정입니다.

class Study(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="타이머", description="공부 메이트와 함께하는 집중 타이머")
    async def timer(self, interaction: discord.Interaction):
        view = StudyTimerView()
        await interaction.response.send_message("누구와 함께 공부하시겠어요?", view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Study(bot))
