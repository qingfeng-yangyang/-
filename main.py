import os
import requests
import smtplib
from email.mime.text import MIMEText

def run_agent():

    email = os.environ["EMAIL"]
    app_password = os.environ["APP_PASSWORD"]
    deepseek_key = os.environ["DEEPSEEK_API_KEY"]

    # ===== 天气 =====
    url = "https://api.open-meteo.com/v1/forecast?latitude=23.12&longitude=114.41&current=temperature_2m,wind_speed_10m,precipitation"
    data = requests.get(url).json()

    temp = data["current"]["temperature_2m"]
    wind = data["current"]["wind_speed_10m"]
    rain = data["current"]["precipitation"]

    # ===== AI（DeepSeek）=====
    prompt = f"""
你是一个生活助手，请根据天气给出出行建议（简洁中文）：

天气数据：
温度：{temp}
风速：{wind}
降雨：{rain}

要求：
- 是否适合出门
- 是否带伞
- 一句总结
"""

    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {deepseek_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
    )

    advice = response.json()["choices"][0]["message"]["content"]

    # ===== 邮件 =====
    msg = MIMEText(advice, "plain", "utf-8")
    msg["Subject"] = "今日AI天气建议"
    msg["From"] = email
    msg["To"] = email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, app_password)
    server.send_message(msg)
    server.quit()

    print("AGENT RUN SUCCESS")

run_agent()
