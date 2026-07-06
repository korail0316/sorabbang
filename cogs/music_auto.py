import discord
from discord.ext import commands

class AutoMusic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_channel = "라운지"

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot: return
        
        # 봇이 뭘 보고 있는지 로그에 출력하게 만듭니다.
        if after.channel:
            print(f"[DEBUG] 현재 접속한 채널 이름: '{after.channel.name}'")
        
        # 이름이 같은지 확인
        if after.channel and after.channel.name == "라운지":
            print("[DEBUG] 채널 일치! 접속 시도...")
            vc = await after.channel.connect()
            await self.play_music(vc)
        elif before.channel and before.channel.name == self.target_channel:
            vc = discord.utils.get(self.bot.voice_clients, guild=member.guild)
            if vc and len(before.channel.members) == 0:
                await vc.disconnect()

async def play_music(self, vc):
        url = "https://drive.google.com/uc?export=download&id=12o-e071uRMl2Hajx9k2JPLfqlMbrN7j6"
        # 'executable' 경로를 추가하여 서버 환경에서 ffmpeg를 확실히 찾게 함
        vc.play(discord.FFmpegPCMAudio(url, executable="ffmpeg", options="-vn"))

async def setup(bot):
    await bot.add_cog(AutoMusic(bot))
