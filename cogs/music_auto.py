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
        # yt_dlp 설정을 최소화하여 차단 방지
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'cookiefile': 'cookies.txt',
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.youtube_url, download=False)
                # 혹시 info가 dict가 아니라 None일 수 있으니 체크
                if info:
                    url = info.get('url')
                    vc.play(discord.FFmpegPCMAudio(url, before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', options='-vn'))
                    print("[성공] 음악 재생 시작!")
                else:
                    print("[오류] 정보 추출 실패!")
        except Exception as e:
            print(f"[상세 오류] {e}")

async def setup(bot):
    await bot.add_cog(AutoMusic(bot))
