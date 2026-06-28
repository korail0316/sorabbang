import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="타이머", description="실시간으로 줄어드는 타이머 패널을 띄웁니다.")
    async def timer(self, interaction: discord.Interaction, 공부시간분: int):
        # 1. 처음에 메시지를 보냅니다.
        await interaction.response.send_message(f"⏱️ **집중 시작!**\n남은 시간: {공부시간분}분 00초")
        
        # 2. 남은 초를 계산합니다.
        total_seconds = 공부시간분 * 60
        
        # 3. 1초씩 줄어들며 메시지를 수정합니다.
        for remaining in range(total_seconds, 0, -1):
            minutes, seconds = divmod(remaining, 60)
            
            # 메시지 업데이트
            await interaction.edit_original_response(
                content=f"⏱️ **집중 중...**\n남은 시간: {minutes}분 {seconds:02d}초"
            )
            await asyncio.sleep(1) # 1초 대기
        
        # 4. 종료 메시지
        await interaction.edit_original_response(
            content="🎉 **공부 끝!** 정말 고생 많으셨습니다. 이제 푹 쉬세요!"
        )

async def setup(bot):
    await bot.add_cog(Timer(bot))
