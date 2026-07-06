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
            vc = await after.channel.connect()
            await self.play_music(vc)
        elif before.channel and before.channel.name == self.target_channel:
            vc = discord.utils.get(self.bot.voice_clients, guild=member.guild)
            if vc and len(before.channel.members) == 0:
                await vc.disconnect()

    async def play_music(self, vc):
        url = "https://drive.google.com/uc?export=download&id=12o-e071uRMl2Hajx9k2JPLfqlMbrN7j6"
        vc.play(discord.FFmpegPCMAudio(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", options="-vn"))

async def setup(bot):
    await bot.add_cog(AutoMusic(bot))
