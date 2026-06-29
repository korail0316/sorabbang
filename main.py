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
    # 명령어 강제 동기화
    synced = await bot.tree.sync()
    print(f'{bot.user} 소라빵 가동 완료! {len(synced)}개의 명령어가 동기화되었습니다.')

bot.run(os.getenv('DISCORD_TOKEN'))
