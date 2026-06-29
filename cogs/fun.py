import discord
from discord.ext import commands
from discord import app_commands
import google.generativeai as genai
import os
import asyncio

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="포춘쿠키", description="AI가 생성하는 오늘의 점괘")
    async def fortune(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        try:
            # 404 에러가 계속 난다면 모델명을 'gemini-1.5-flash' 혹은 'gemini-1.5-pro'로 바꿔보세요.
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            loop = asyncio.get_event_loop()
            response = await asyncio.wait_for(
                loop.run_in_executor(None, lambda: model.generate_content("시험 기간 학생에게 주는 격려와 행운의 점괘를 짧게 1문장으로 써줘.")),
                timeout=8.0
            )
            
            embed = discord.Embed(title="🥠 AI 소라빵의 점괘", description=response.text, color=discord.Color.gold())
            await interaction.followup.send(embed=embed)
            
        except asyncio.TimeoutError:
            await interaction.followup.send("🥠 AI가 너무 깊게 고민하네요... 오늘은 노력한 만큼 반드시 결과가 나올 거예요!")
        except Exception as e:
            await interaction.followup.send("🥠 AI가 잠시 낮잠 중이네요... 오늘은 노력한 만큼 반드시 결과가 나올 거예요!")
            print(f"AI 에러 발생: {e}")

async def setup(bot):
    await bot.add_cog(Fun(bot))
