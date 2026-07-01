import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw
import io

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_calendar_image(self, schedules):
        # 1. 800x600 사이즈의 깔끔한 흰색 배경 이미지 생성
        img = Image.new('RGB', (800, 600), color=(240, 240, 240))
        d = ImageDraw.Draw(img)
        
        # 2. 제목 그리기
        d.text((50, 30), "STUDY CAFE SCHEDULE", fill=(50, 50, 50))
        
        # 3. 일정 목록 그리기 (여기에 나중에 DB 연동)
        y_offset = 100
        for schedule in schedules:
            d.text((50, y_offset), f"• {schedule}", fill=(0, 0, 0))
            y_offset += 40
            
        # 4. 메모리에 저장하여 전송 준비
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return buf

    @app_commands.command(name="캘린더", description="스터디 카페 일정표를 이미지로 확인합니다.")
    async def view_calendar(self, interaction: discord.Interaction):
        # 임시 데이터 (나중에 이 부분을 DB에서 불러오게 할 예정)
        temp_schedules = ["07-05 14:00 - 그룹 스터디", "07-10 10:00 - 모의고사"]
        
        image_buf = self.create_calendar_image(temp_schedules)
        file = discord.File(fp=image_buf, filename="calendar.png")
        
        embed = discord.Embed(title="📅 이번 주 스터디 일정", color=discord.Color.blue())
        embed.set_image(url="attachment://calendar.png")
        
        await interaction.response.send_message(embed=embed, file=file)

async def setup(bot):
    await bot.add_cog(Schedule(bot))
