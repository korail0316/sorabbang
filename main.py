import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# 1. 권한(intents) 정의
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# 2. 봇 객체 생성 (오타 수정됨: intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # 기존 코드 아래에 이 두 줄을 추가하세요
    await bot.load_extension('cogs.fun')
    await bot.load_extension('cogs.timer')
    
    await bot.tree.sync()
    print(f'{bot.user} 소라빵이 가동되었습니다.')

bot.run(os.getenv('DISCORD_TOKEN'))
