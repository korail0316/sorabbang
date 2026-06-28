import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=bot_intents) # 이 부분 수정

@bot.event
async def on_ready():
    # cogs 폴더에서 fun.py를 불러오기
    await bot.load_extension('cogs.fun')
    await bot.tree.sync() # 명령어 동기화
    print(f'{bot.user} 소라빵이 가동되었습니다.')

bot.run(os.getenv('DISCORD_TOKEN'))
