import discord
from discord.ext import commands
from discord import app_commands
import google.generativeai as genai
import os
import asyncio

# 환경 변수에서 API 키 로드
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="포춘쿠키", description="AI가 생성하는 오늘의 점괘")
    async def fortune(self, interaction: discord.Interaction):
        # 작업이 오래 걸릴 수 있으므로 미리 '생각 중...' 표시
        await interaction.response.defer()
        
        try:
            # 로그에서 확인된 models/gemini-3.5-flash 사용
            model = genai.GenerativeModel('gemini-3.5-flash')
            
            # API 호출이 동기 방식이므로 비동기 환경에서 실행
            loop = asyncio.get_event_loop()
            prompt = "시험 기간 학생에게 주는 격려와 행운의 점괘를 짧게 1문장으로 써줘."
            
            # 8초 타임아웃 설정
            response = await asyncio.wait_for(
                loop.run_in_executor(None, lambda: model.generate_content(prompt)),
                timeout=8.0
            )
            
            # 결과 전송
            embed = discord.Embed(
                title="🥠 당신을 위한 당신의 운세", 
                description=response.text, 
                color=discord.Color.gold()
            )
            await interaction.followup.send(embed=embed)
            
        except asyncio.TimeoutError:
            await interaction.followup.send("🥠 AI가 너무 깊게 고민하네요... 오늘은 노력한 만큼 반드시 결과가 나올 거예요!")
        except Exception as e:
            # 에러 발생 시 로그 출력 및 사용자 안내
            print(f"AI 에러 발생 상세: {e}")
            await interaction.followup.send("🥠 AI가 잠시 낮잠 중이네요... 오늘은 노력한 만큼 반드시 결과가 나올 거예요!")

async def setup(bot):
    await bot.add_cog(Fun(bot))
