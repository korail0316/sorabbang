import discord
from discord.ext import commands
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# 1. 봇 설정
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 2. 봇이 켜졌을 때
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'소라빵이 온라인입니다: {bot.user}')

# 3. 테스트 명령어 (이게 잘 되면 기능 추가할 예정)
@bot.tree.command(name="안녕", description="소라빵과 인사해요")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("안녕! 소라빵이야. 오늘도 힘내자!")

# 4. 봇 실행
# Railway의 Variables에 DISCORD_TOKEN을 설정해두셨죠? 그걸 그대로 씁니다.
bot.run(os.environ['DISCORD_TOKEN'])
