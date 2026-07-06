import discord
from discord.ext import commands

class AutoMusic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot: return
        
        # 1. 채널 감지 디버깅
        if after.channel:
            print(f"[DEBUG] 접속한 채널명: '{after.channel.name}'")
            
            if after.channel.name == "라운지":
                print("[DEBUG] '라운지' 채널 일치 확인. 연결 시도...")
                voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
                
                if not voice_client:
                    vc = await after.channel.connect()
                    await self.play_music(vc)

    async def play_music(self, vc):
        url = "https://drive.google.com/uc?export=download&id=12o-e071uRMl2Hajx9k2JPLfqlMbrN7j6"
        ffmpeg_opts = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        
        try:
            # FFmpeg 경로를 명시하고 재생
            source = discord.FFmpegPCMAudio(url, executable="ffmpeg", **ffmpeg_opts)
            vc.play(source)
            print("[성공] 음악 재생 명령어 전달 완료!")
        except Exception as e:
            print(f"[재생 오류 발생] {e}")

async def setup(bot):
    await bot.add_cog(AutoMusic(bot))
