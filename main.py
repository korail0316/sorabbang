import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv() # .env 파일에서 토큰을 읽어오라는 뜻입니다.

# 봇 권한 설정 (메시지 읽기 등)
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} 소라빵이 서버에 들어왔어요!')

@bot.command()
async def 안녕(ctx):
    await ctx.send("안녕! 나는 따뜻한 소라빵이야.")

bot.run(os.getenv('DISCORD_TOKEN'))