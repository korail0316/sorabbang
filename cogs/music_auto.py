import discord
from discord.ext import commands
import yt_dlp
import asyncio

class AutoMusic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_channel = "라운지"

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot: return

        # 1. 누군가 채널에 들어오거나 나갔을 때 로그 출력
        channel_name = after.channel.name if after.channel else (before.channel.name if before.channel else "알 수 없음")
        print(f"[DEBUG] {member.name} 상태 변경: {channel_name} 채널")

        if after.channel and after.channel.name == self.target_channel:
            print(f"[DEBUG] 타겟 채널({self.target_channel}) 입장 감지됨")
            voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
            if not voice_client:
                try:
                    vc = await after.channel.connect()
                    print(f"[DEBUG] {self.target_channel} 채널 접속 성공!")
                    # 테스트용 재생 (생략 가능)
                except Exception as e:
                    print(f"[ERROR] 채널 접속 실패: {e}")
        
        elif before.channel and before.channel.name == self.target_channel:
            voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
            if voice_client and len(before.channel.members) == 1:
                print(f"[DEBUG] 채널에 혼자 남음, 퇴장합니다.")
                await voice_client.disconnect()

    async def play_music(self, vc):
        try:
            loop = self.bot.loop
            print("[DEBUG] 오디오 추출 시작...")
            data = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ytdl_opts).extract_info(self.youtube_url, download=False))
            url = data['https://youtu.be/kagoEGKHZvU?si=kJCr1GTOOcC47IH0']
            print(f"[DEBUG] 오디오 URL 추출 성공: {url}")
            
            ffmpeg_opts = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
                'options': '-vn'
            }
            # 재생 시도
            vc.play(discord.FFmpegPCMAudio(url, **ffmpeg_opts), after=lambda e: print(f"[DEBUG] 재생 종료 혹은 오류: {e}"))
            print("[DEBUG] 재생 명령 전달 완료!")
        except Exception as e:
            print(f"[ERROR] 재생 실패: {e}")

async def setup(bot):
    await bot.add_cog(AutoMusic(bot))
    print("AutoMusic 기능이 로드되었습니다.")
