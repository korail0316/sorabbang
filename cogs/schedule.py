import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw
import io
import json
import os

DATA_FILE = "schedule_data.json"

def load_schedules():
    if not os.path.exists(DATA_FILE): return []
    with open(DATA_FILE, "r", encoding="utf-8") as f: return json.load(f)

def save_schedule(new_entry):
    data = load_schedules()
    data.append(new_entry)
    with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(data, f, indent=4, ensure_ascii=False)

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_calendar_image(self):
        schedules = load_schedules()
        img = Image.new('RGB', (800, 600), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        
        d.text((50, 30), "STUDY CAFE SCHEDULE", fill=(0, 0, 0))
        
        y_offset = 100
        for item in schedules:
            d.text((50, y_offset), f"• {item['date']} | {item['content']}", fill=(0, 0, 0))
            y_offset += 40
            
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return buf

    @app_commands.command(name="일정추가", description="일정을 등록합니다.")
    async def add_schedule(self, interaction: discord.Interaction, date: str, content: str):
        save_schedule({"date": date, "content": content})
        await interaction.response.send_message(f"✅ {date} 일정이 저장되었습니다!", ephemeral=True)

    @app_commands.command(name="캘린더", description="저장된 일정을 이미지로 확인합니다.")
    async def view_calendar(self, interaction: discord.Interaction):
        image_buf = self.create_calendar_image()
        file = discord.File(fp=image_buf, filename="calendar.png")
        
        embed = discord.Embed(title="📅 이번 주 스터디 일정", color=discord.Color.blue())
        embed.set_image(url="attachment://calendar.png")
        await interaction.response.send_message(embed=embed, file=file)

async def setup(bot):
    await bot.add_cog(Schedule(bot))
