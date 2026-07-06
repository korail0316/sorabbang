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
        # yt-dlp 추출 과정 전체를 삭제하고 파일만 재생
        try:
            vc.play(discord.FFmpegPCMAudio('music.mp3'))
            print("[성공] 로컬 파일 재생 시작!")
        except Exception as e:
            print(f"[재생 오류] {e}")

async def setup(bot):
    await bot.add_cog(AutoMusic(bot))
