import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="타이머", description="공부 시간과 휴식 시간을 설정해서 함께 집중해요!")
    async def timer(self, interaction: discord.Interaction, 공부시간분: int, 휴식시간분: int):
        # 공부 시작 메시지
        await interaction.response.send_message(f"⏱️ {interaction.user.mention}님, {공부시간분}분 동안 집중 시작합니다!")
        
        # 공부 시간 대기
        await asyncio.sleep(공부시간분 * 60)
        
        # 공부 끝, 휴식 시작 알림
        await interaction.followup.send(f"🔔 {interaction.user.mention}님, {공부시간분}분이 지났어요! 이제 {휴식시간분}분 동안 휴식하세요!")
        
        # 휴식 시간 대기
        await asyncio.sleep(휴식시간분 * 60)
        
        # 휴식 끝 알림
        await interaction.followup.send(f"✅ {interaction.user.mention}님, 휴식 시간이 끝났습니다. 다시 힘내볼까요?")

async def setup(bot):
    await bot.add_cog(Timer(bot))
