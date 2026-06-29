import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class TimeInputModal(discord.ui.Modal, title='집중 시간 설정'):
    minutes = discord.ui.TextInput(label='공부할 시간(분)', placeholder='예: 50', min_length=1, max_length=3)

    def __init__(self, selected_users):
        super().__init__()
        self.selected_users = selected_users

    async def on_submit(self, interaction: discord.Interaction):
        time_val = int(self.minutes.value)
        total_seconds = time_val * 60
        user_names = ", ".join([user.mention for user in self.selected_users])
        
        # 1. 시작 메시지 전송
        embed = discord.Embed(
            title="⏱️ 타이머 준비 중...",
            description=f"**메이트:** {user_names}\n\n## {time_val}분 설정 완료!\n3초 뒤에 시작합니다.",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()

        # 2. 3초 대기
        await asyncio.sleep(3)

        # 3. 타이머 루프 시작
        embed.title = "⏱️ 공부 타이머 가동 중"
        for remaining in range(total_seconds, -1, -1):
            hours, remainder = divmod(remaining, 3600)
            mins, secs = divmod(remainder, 60)
            timer_str = f"{hours:02d}:{mins:02d}:{secs:02d}"

            embed.description = f"**메이트:** {user_names}\n\n## {timer_str}"
            await message.edit(embed=embed)
            await asyncio.sleep(1)

        # 4. 종료
        embed.title = "✅ 타이머 종료"
        embed.description = f"**메이트:** {user_names}\n\n## 00:00:00\n공부 세션이 종료되었습니다!"
        await message.edit(embed=embed)

class MemberSelect(discord.ui.UserSelect):
    def __init__(self):
        super().__init__(placeholder="메이트 선택...", min_values=1, max_values=5)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TimeInputModal(self.values))

class StudyTimerView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(MemberSelect())

class Study(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 'minutes' 인자 제거, 명령어 단순화
    @app_commands.command(name="타이머", description="공부 메이트와 함께하는 집중 타이머")
    async def timer(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📚 스터디 세션 설정",
            description="메이트를 선택하여 타이머를 시작하세요.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, view=StudyTimerView(), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Study(bot))
