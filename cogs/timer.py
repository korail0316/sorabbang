import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 타이머 작업을 별도로 분리하는 함수
    async def run_timer(self, interaction: discord.Interaction, total_seconds: int):
        embed = discord.Embed(title="⏱️ 소라빵 타이머", color=discord.Color.blue())
        
        for remaining in range(total_seconds, -1, -5):
            h, rem = divmod(remaining, 3600)
            m, s = divmod(rem, 60)
            time_str = f"{h:02d}:{m:02d}:{s:02d}"
            
            if remaining > 0:
                embed.description = f"남은 시간: {time_str}"
            else:
                embed.description = "타이머 종료"
            
            # 메시지 수정 시도
            try:
                await interaction.edit_original_response(embed=embed)
            except Exception as e:
                print(f"메시지 수정 오류: {e}")
                break
                
            if remaining > 0:
                await asyncio.sleep(5)

    @app_commands.command(name="타이머", description="타이머를 시작합니다.")
    async def timer(self, interaction: discord.Interaction, 분: int):
        # 1. 즉시 응답 (이게 없으면 오류 발생)
        await interaction.response.send_message("타이머를 시작합니다!")
        
        # 2. 타이머를 백그라운드 작업으로 실행
        asyncio.create_task(self.run_timer(interaction, 분 * 60))

async def setup(bot):
    await bot.add_cog(Timer(bot))
