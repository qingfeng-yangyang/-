import requests
import smtplib
from email.mime.text import MIMEText
import os

def run_agent():

    email = os.environ.get("EMAIL")
    app_password = os.environ.get("APP_PASSWORD")

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 23.7437,
        "longitude": 114.7000,
        "current_weather": True
    }

    data = requests.get(url, params=params).json()
    weather = data["current_weather"]
    temp = data["current"]["temperature"]
    rain = data["current"].get("precipitation", 0)
temp = data["current"]["temperature"]
wind = data["current"]["wind_speed"]

# 智能建议
advice = []

if rain > 50:
    advice.append("今天降雨概率较高，建议带伞 ☔")

if temp > 30:
    advice.append("天气较热，注意防晒 🧴")
elif temp < 15:
    advice.append("天气较冷，注意保暖 🧥")

if wind > 8:
    advice.append("风较大，注意出行安全 🌬")

if not advice:
    advice.append("天气良好，正常出行即可 👍")
    windspeed = weather["windspeed"]

    tips = []

    if temperature >= 30:
        tips.append("🔥 天气较热，注意防晒")
    elif temperature <= 15:
        tips.append("🧥 天气较冷，注意保暖")
    else:
        tips.append("🙂 温度适中")

    if windspeed >= 20:
        tips.append("💨 风较大，注意安全")

    content = f"""📍河源今日天气

🌡 温度：{temperature}°C
💨 风速：{windspeed} km/h

🧠 建议：
""" + "\n".join(tips)

    msg = MIMEText(content)
    message = f"""
📍 今日天气

🌡 温度：{temp}°C
💨 风速：{wind} m/s
🌧 降雨概率：{rain}%

🧠 建议：
{chr(10).join(advice)}
"""
    msg["From"] = email
    msg["To"] = email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(email, app_password)
    server.send_message(msg)
    server.quit()

    print("OK")

if __name__ == "__main__":
    run_agent()
print("AGENT RUN SUCCESS")
import os

email = os.environ["EMAIL"]
app_password = os.environ["APP_PASSWORD"]
#GitHub Actions 自动跑
