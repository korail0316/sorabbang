import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="타이머", description="1초마다 갱신되는 집중 타이머")
    async def timer(self, interaction: discord.Interaction, 분: int):
        await interaction.response.send_message("⏱️ 집중 시작!")
        
        total_seconds = 분 * 60
        embed = discord.Embed(title="⏱️ 소라스터디 집중 시간", color=discord.Color.blue())
        
        for remaining in range(total_seconds, -1, -1):
            h, rem = divmod(remaining, 3600)
            m, s = divmod(rem, 60)
            # 큰 글씨(Markdown #) 적용
            time_str = f"# {h:02d}:{m:02d}:{s:02d}"
            
            embed.description = f"남은 시간:\n{time_str}"
            
            try:
                await interaction.edit_original_response(embed=embed)
            except:
                break
            await asyncio.sleep(1) # 1초 갱신
        
        await interaction.edit_original_response(content="🎉 끝!", embed=None)

async def setup(bot):
    await bot.add_cog(Timer(bot))
