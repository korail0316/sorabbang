import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # 여기서 cogs를 불러옵니다.
    await bot.load_extension('cogs.fun')
    await bot.load_extension('cogs.timer')
    
    # 이 부분이 가장 중요합니다! 명령어를 디스코드 서버에 동기화합니다.
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)}개의 명령어가 동기화되었습니다.")
    except Exception as e:
        print(f"동기화 오류: {e}")
        
    print(f'{bot.user} 소라빵이 가동되었습니다.')

bot.run(os.getenv('DISCORD_TOKEN'))
