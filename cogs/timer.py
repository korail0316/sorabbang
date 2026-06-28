import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="타이머", description="공부 타이머를 시작합니다.")
    async def timer(self, interaction: discord.Interaction, 분: int):
        # 1. 일단 즉시 응답을 보냅니다 (이걸 안 하면 오류가 납니다)
        embed = discord.Embed(
            title="⏱️ 소라스터디 집중 시간",
            description=f"준비 중...",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)
        
        total_seconds = 분 * 60
        
        # 2. 이후 패널을 갱신합니다
        for remaining in range(total_seconds, -1, -5): # 0초까지 포함
            h, rem = divmod(remaining, 3600)
            m, s = divmod(rem, 60)
            time_str = f"{h:02d}:{m:02d}:{s:02d}"
            
            if remaining > 0:
                embed.description = f"남은 시간: {time_str}"
            else:
                embed.description = "🎉 **공부 끝!** 고생 많으셨습니다."
                
            await interaction.edit_original_response(embed=embed)
            
            if remaining > 0:
                await asyncio.sleep(5)

async def setup(bot):
    await bot.add_cog(Timer(bot))
