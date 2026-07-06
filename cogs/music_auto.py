import discord
from discord.ext import commands
import yt_dlp

class AutoMusic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_channel = "라운지"
        self.youtube_url = "https://www.youtube.com/watch?v=kagoEGKHZvU"

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot: return

        # 채널 입장 시 연결 및 재생
        if after.channel and after.channel.name == self.target_channel:
            voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
            if not voice_client:
                vc = await after.channel.connect()
                await self.play_music(vc)
        
        # 채널 혼자 남을 시 퇴장
        elif before.channel and before.channel.name == self.target_channel:
            voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
            if voice_client and len(before.channel.members) == 1:
                await voice_client.disconnect()

async def play_music(self, vc):
        # 방금 만든 직접 다운로드 링크
        direct_url = "https://drive.google.com/uc?export=download&id=12o-e071uRMl2Hajx9k2JPLfqlMbrN7j6"
        
        ffmpeg_opts = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
            'options': '-vn'
        }
        
        try:
            # 재생 시도
            vc.play(discord.FFmpegPCMAudio(direct_url, **ffmpeg_opts))
            print("[성공] 구글 드라이브 음악 재생 시작!")
        except Exception as e:
            print(f"[재생 오류] {e}")

async def setup(bot):
    await bot.add_cog(AutoMusic(bot))
