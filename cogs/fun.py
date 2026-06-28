import discord
from discord import app_commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="포춘쿠키", description="소라빵이 시험 기간 행운의 점괘를 봐줘요!")
    async def fortune(self, interaction: discord.Interaction):
        messages = [
            "노력한 만큼 결과가 반드시 나올 거예요. 자신감을 가지세요!",
            "잠시 쉬어가도 괜찮아요. 당신은 지금도 충분히 잘하고 있어요.",
            "오늘 공부한 부분에서 시험 문제가 나옵니다! 다시 한번 훑어보세요.",
            "실수할 수 있으니 꼼꼼히 확인하세요. 급할수록 천천히!",
            "막 찍어도 정답이 보일 거예요! 운이 당신과 함께합니다."
        ]
        
        # 임베드 만들기
        embed = discord.Embed(
            title="🥠 소라빵의 오늘의 점괘",
            description=random.choice(messages),
            color=discord.Color.blue() # 왼쪽 파란 선 색상 설정
        )
        embed.set_footer(text="공부하느라 고생했어요!")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))
