import os
import requests
import smtplib
from email.mime.text import MIMEText

def run_agent():
    # ====== 1. 读取环境变量 ======
    email = os.environ["EMAIL"]
    app_password = os.environ["APP_PASSWORD"]

    # ====== 2. 天气 API（你如果已经有URL就换这里）======
    url = "https://api.open-meteo.com/v1/forecast?latitude=23.12&longitude=114.41&current=temperature_2m,wind_speed_10m,precipitation"

    response = requests.get(url)
    data = response.json()

    # ====== 3. 提取数据 ======
    temp = data["current"]["temperature_2m"]
    wind = data["current"]["wind_speed_10m"]
    rain = data["current"]["precipitation"]

    # ====== 4. 智能建议 ======
    advice = []

    if rain > 0.5:
        advice.append("今天可能下雨，建议带伞 ☔")

    if temp > 30:
        advice.append("天气较热，注意防晒 🧴")
    elif temp < 15:
        advice.append("天气较冷，注意保暖 🧥")

    if wind > 8:
        advice.append("风较大，注意安全 🌬")

    if not advice:
        advice.append("天气不错，正常出行 👍")

    # ====== 5. 邮件内容 ======
    message = f"""
📍 今日天气

🌡 温度：{temp}°C
💨 风速：{wind} m/s
🌧 降雨：{rain}

🧠 建议：
{chr(10).join(advice)}
"""

    # ====== 6. 发邮件 ======
    msg = MIMEText(message, "plain", "utf-8")
    msg["Subject"] = "今日天气提醒"
    msg["From"] = email
    msg["To"] = email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, app_password)
    server.send_message(msg)
    server.quit()

    print("AGENT RUN SUCCESS")

run_agent()
