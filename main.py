import discord
from discord.ext import commands
import os
import asyncio

# 봇 기본 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Cog 파일들을 자동으로 로드하는 함수
async def load_extensions():
    # cogs 폴더에 있는 모든 파이썬 파일 로드
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("DISCORD_TOKEN"))

@bot.event
async def on_ready():
    # 이 코드가 중요합니다. 기존에 등록된 모든 명령어를 지우고 지금 코드에 있는 것만 남깁니다.
    await bot.tree.sync() 
    print(f'{bot.user}으로 로그인 및 명령어 동기화 완료!')

if __name__ == '__main__':
    asyncio.run(main())
