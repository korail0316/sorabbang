import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="타이머", description="공부 타이머를 시작합니다.")
    async def timer(self, interaction: discord.Interaction, 분: int):
        await interaction.response.send_message("⏱️ 타이머를 시작합니다!")
        
        embed = discord.Embed(title="⏱️ 집중 시간", description=f"남은 시간: 00:{분:02d}:00", color=discord.Color.blue())
        msg = await interaction.original_response()
        
        for i in range(분 * 60, -1, -10): # 10초 단위 갱신으로 안전성 확보
            h, m, s = i // 3600, (i % 3600) // 60, i % 60
            embed.description = f"남은 시간: {h:02d}:{m:02d}:{s:02d}"
            await interaction.edit_original_response(embed=embed)
            await asyncio.sleep(10)
        
        await interaction.edit_original_response(content="🎉 끝!", embed=None)

async def setup(bot):
    await bot.add_cog(Timer(bot))
