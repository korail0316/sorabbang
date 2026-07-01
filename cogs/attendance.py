import discord
from discord.ext import commands
from discord import app_commands
import json
import datetime
import os

# 데이터 파일 경로
DATA_FILE = "attendance_data.json"

def load_data():
    if not os.path.exists(DATA_FILE): return {}
    with open(DATA_FILE, "r") as f: return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

class Attendance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="출석", description="오늘의 공부 출석을 체크합니다.")
    async def attendance(self, interaction: discord.Interaction):
        data = load_data()
        user_id = str(interaction.user.id)
        today = datetime.date.today().isoformat()
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

        user_info = data.get(user_id, {"last_date": None, "streak": 0})

        # 이미 출석했는지 확인
        if user_info["last_date"] == today:
            await interaction.response.send_message("이미 오늘 출석하셨습니다!", ephemeral=True)
            return

        # 연속 출석 처리
        if user_info["last_date"] == yesterday:
            user_info["streak"] += 1
        else:
            user_info["streak"] = 1
        
        user_info["last_date"] = today
        data[user_id] = user_info
        save_data(data)

        embed = discord.Embed(
            title="✅ 출석 완료!",
            description=f"오늘도 열심히 달려봅시다!\n\n현재 **연속 {user_info['streak']}일**째 공부 중입니다.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Attendance(bot))
