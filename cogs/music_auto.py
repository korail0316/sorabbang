import discord
from discord.ext import commands

class AutoMusic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_channel = "라운지"

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot: return

        if after.channel and after.channel.name == self.target_channel:
            voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
            if not voice_client:
                vc = await after.channel.connect()
                await self.play_music(vc) # 여기서 호출!
        
        elif before.channel and before.channel.name == self.target_channel:
            voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
            if voice_client and len(before.channel.members) == 1:
                await voice_client.disconnect()

    # 이 부분이 클래스 안으로 들어와야 합니다!
    async def play_music(self, vc):
        direct_url = "https://drive.google.com/file/d/12o-e071uRMl2Hajx9k2JPLfqlMbrN7j6"
        ffmpeg_opts = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
            'options': '-vn'
        }
        try:
            vc.play(discord.FFmpegPCMAudio(direct_url, **ffmpeg_opts))
            print("[성공] 구글 드라이브 음악 재생 시작!")
        except Exception as e:
            print(f"[재생 오류] {e}")

async def setup(bot):
    await bot.add_cog(AutoMusic(bot))
