import discord
from discord.ext import commands
import yt_dlp
import asyncio

# cogs/music_auto.py 파일의 윗부분
ytdl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'cookiefile': 'cookies.txt',
    # 아래 설정들을 추가하여 브라우저인 것처럼 위장합니다
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'ignoreerrors': True,
    'no_warnings': True,
}

class AutoMusic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_channel = "라운지"
        self.youtube_url = "https://youtu.be/kagoEGKHZvU" # 여기에 링크를 넣으세요

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot: return

        if after.channel and after.channel.name == self.target_channel:
            voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
            if not voice_client:
                vc = await after.channel.connect()
                await self.play_music(vc)
        
        elif before.channel and before.channel.name == self.target_channel:
            voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
            if voice_client and len(before.channel.members) == 1:
                await voice_client.disconnect()

    async def play_music(self, vc):
        try:
            loop = self.bot.loop
            # 링크에서 오디오 정보 추출
            data = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ytdl_opts).extract_info(self.youtube_url, download=False))
            url = data['url'] # 이게 핵심입니다!
            
            ffmpeg_opts = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
                'options': '-vn'
            }
            vc.play(discord.FFmpegPCMAudio(url, **ffmpeg_opts))
        except Exception as e:
            print(f"[ERROR] 재생 실패: {e}")

async def setup(bot):
    await bot.add_cog(AutoMusic(bot))
