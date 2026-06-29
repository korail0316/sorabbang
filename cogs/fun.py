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
            # 사용 가능한 모델 목록을 로그에 출력하여 확인합니다.
            # 이 코드는 어떤 모델을 써야 할지 알려줍니다.
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"사용 가능한 모델 이름: {m.name}")
            
            # 현재 에러가 난 'gemini-1.5-flash' 대신, 
            # 로그에 찍힐 '사용 가능한 모델 이름' 중 하나를 아래에 넣으세요.
            model = genai.GenerativeModel('gemini-1.5-flash') 
            
            loop = asyncio.get_event_loop()
            response = await asyncio.wait_for(
                loop.run_in_executor(None, lambda: model.generate_content("시험 기간 학생에게 주는 격려와 행운의 점괘를 짧게 1문장으로 써줘.")),
                timeout=8.0
            )
            
            embed = discord.Embed(title="🥠 AI 소라빵의 점괘", description=response.text, color=discord.Color.gold())
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            # 여기서 에러 로그를 확인하고, 위에서 출력된 '사용 가능한 모델'로 이름을 바꿔야 합니다.
            await interaction.followup.send("🥠 AI가 잠시 낮잠 중이네요... 오늘은 노력한 만큼 반드시 결과가 나올 거예요!")
            print(f"AI 에러 발생 상세: {e}")

async def setup(bot):
    await bot.add_cog(Fun(bot))
