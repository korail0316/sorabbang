import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont # 폰트 사용 추천
import io
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "schedule_data.json")
TEMPLATE_PATH = os.path.join(BASE_DIR, "calendar_template.png") # 배경 이미지 경로

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def draw_calendar(self):
        # 1. 배경 이미지 로드 (없으면 흰색 바탕 생성)
        if os.path.exists(TEMPLATE_PATH):
            img = Image.open(TEMPLATE_PATH)
        else:
            img = Image.new('RGB', (800, 600), color=(255, 255, 255))
        
        d = ImageDraw.Draw(img)
        data = self.load_schedules()
        
        # 2. 데이터 시각화
        y_offset = 100
        for item in data:
            # 배경 위에 텍스트 입력
            d.text((50, y_offset), f"{item['date']} - {item['content']}", fill=(0, 0, 0))
            y_offset += 40
            
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return buf

    def load_schedules(self):
        if not os.path.exists(DATA_FILE): return []
        with open(DATA_FILE, "r", encoding="utf-8") as f: return json.load(f)

    @app_commands.command(name="일정추가", description="대표 캘린더에 일정을 추가합니다.")
    async def add_schedule(self, interaction: discord.Interaction, date: str, content: str):
        data = self.load_schedules()
        data.append({"date": date, "content": content})
        with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(data, f, indent=4, ensure_ascii=False)
        
        await interaction.response.send_message(f"✅ {date} 일정이 캘린더에 추가되었습니다!", ephemeral=True)

    @app_commands.command(name="캘린더", description="대표 캘린더를 확인합니다.")
    async def view_calendar(self, interaction: discord.Interaction):
        image_buf = self.draw_calendar()
        file = discord.File(fp=image_buf, filename="calendar.png")
        
        embed = discord.Embed(title="📅 스터디 대표 캘린더", color=discord.Color.blue())
        embed.set_image(url="attachment://calendar.png")
        await interaction.response.send_message(embed=embed, file=file)

async def setup(bot):
    await bot.add_cog(Schedule(bot))
