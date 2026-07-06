import discord
from discord.ext import commands
import yt_dlp
import asyncio

# 유튜브 오디오 추출 설정
ytdl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
}

class AutoMusic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_channel = "라운지"
        self.youtube_url = "https://youtu.be/XXV9AfI93kU"

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # 봇 자신은 무시
        if member.bot:
            return

        # 1. '라운지' 채널에 입장 시
        if after.channel and after.channel.name == self.target_channel:
            voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
            if not voice_client:
                vc = await after.channel.connect()
                await self.play_music(vc)

        # 2. '라운지' 채널에서 나갈 시 (봇 혼자 남으면 나감)
        elif before.channel and before.channel.name == self.target_channel:
            voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
            if voice_client and len(before.channel.members) == 1:
                await voice_client.disconnect()

    async def play_music(self, vc):
        loop = self.bot.loop
        # 오디오 스트림 URL 추출
        data = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ytdl_opts).extract_info(self.youtube_url, download=False))
        url = data['url']
        
        # 오디오 재생 (FFmpeg)
        ffmpeg_opts = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
            'options': '-vn'
        }
        vc.play(discord.FFmpegPCMAudio(url, **ffmpeg_opts))

async def setup(bot):
    await bot.add_cog(AutoMusic(bot))
