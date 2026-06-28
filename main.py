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

    temperature = weather["temperature"]
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
    msg["Subject"] = "河源天气 Agent"
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
