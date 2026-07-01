import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
import io

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_calendar_image(self, schedules):
        # 1. 빈 이미지 생성 (배경)
        img = Image.new('RGB', (800, 600), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        
        # 2. 텍스트 그리기 (간단한 예시)
        d.text((50, 50), "STUDY CALENDAR", fill=(0, 0, 0))
        for i, schedule in enumerate(schedules):
            d.text((50, 100 + (i * 30)), f"- {schedule}", fill=(0, 0, 0))
            
        # 3. 메모리에 저장
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return buf

    @app_commands.command(name="캘린더", description="시각적 캘린더 이미지를 보여줍니다.")
    async def view_calendar(self, interaction: discord.Interaction):
        # 예시 일정 (나중에 DB에서 가져오도록 수정 예정)
        schedules = ["07-05: 중간고사 준비", "07-10: 그룹 스터디"]
        
        image_buf = self.create_calendar_image(schedules)
        file = discord.File(fp=image_buf, filename="calendar.png")
        
        embed = discord.Embed(title="📅 이번 달 스케줄", color=discord.Color.blue())
        embed.set_image(url="attachment://calendar.png")
        
        await interaction.response.send_message(embed=embed, file=file)

async def setup(bot):
    await bot.add_cog(Schedule(bot))
