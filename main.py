import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    # cogs 파일들을 순서대로 로드
    await bot.load_extension('cogs.fun')
    await bot.load_extension('cogs.timer')

@bot.event
async def on_ready():
    await load_extensions()
    await bot.tree.sync() # 명령어 동기화
    print(f'{bot.user} 소라빵이 가동되었습니다.')

bot.run(os.getenv('DISCORD_TOKEN'))
