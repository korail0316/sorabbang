import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="타이머", description="공부 타이머를 시작합니다.")
    async def timer(self, interaction: discord.Interaction, 분: int):
        total_seconds = 분 * 60
        
        # 1. 초기 임베드 생성
        embed = discord.Embed(
            title="⏱️ 소라스터디 집중 시간",
            description=f"남은 시간: 00:{분:02d}:00",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)
        
        # 2. 5초마다 업데이트 (디스코드 제한 방지)
        for remaining in range(total_seconds, 0, -5):
            h, rem = divmod(remaining, 3600)
            m, s = divmod(rem, 60)
            
            # 시간 형식: 00:00:00
            time_str = f"{h:02d}:{m:02d}:{s:02d}"
            
            # 임베드 수정
            embed.description = f"남은 시간: {time_str}"
            await interaction.edit_original_response(embed=embed)
            
            await asyncio.sleep(5) # 5초 간격 업데이트
        
        # 3. 종료 메시지
        embed.description = "🎉 **공부 끝!** 고생 많으셨습니다."
        await interaction.edit_original_response(embed=embed)

async def setup(bot):
    await bot.add_cog(Timer(bot))
