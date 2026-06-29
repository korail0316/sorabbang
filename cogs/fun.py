import discord
from discord.ext import commands
from discord import app_commands
import google.generativeai as genai
import os

# Gemini API 설정 (환경변수에 GEMINI_API_KEY가 필요합니다)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="포춘쿠키", description="오늘의 운세")
    async def fortune(self, interaction: discord.Interaction):
        await interaction.response.defer() # 응답 대기 시간 확보
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("시험 기간 학생에게 주는 격려와 행운의 점괘를 짧게 1문장으로 써줘.")
        
        embed = discord.Embed(title="🥠 오늘의 운세", description=response.text, color=discord.Color.gold())
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))
