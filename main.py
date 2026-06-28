import os
import requests
import smtplib
from email.mime.text import MIMEText

def run_agent():

    # ===== 环境变量 =====
    email = os.environ["EMAIL"]
    app_password = os.environ["APP_PASSWORD"]
    ark_key = os.environ["ARK_API_KEY"]
    endpoint = os.environ["ARK_ENDPOINT"]

    # ===== 天气 =====
    url = "https://api.open-meteo.com/v1/forecast?latitude=23.12&longitude=114.41&current=temperature_2m,wind_speed_10m,precipitation"
    data = requests.get(url).json()

    temp = data["current"]["temperature_2m"]
    wind = data["current"]["wind_speed_10m"]
    rain = data["current"]["precipitation"]

    # ===== Prompt =====
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

    # ===== 豆包 EP API =====
    response = requests.post(
        f"https://ark.cn-beijing.volces.com/api/v3/{endpoint}/chat/completions",
        headers={
            "Authorization": f"Bearer {ark_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "doubao-lite-4k",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
    )

    res = response.json()

    # ===== 调试输出（GitHub Actions里看）=====
    print("DEBUG STATUS:", response.status_code)
    print("DEBUG RESPONSE:", res)

    # ===== 安全解析 =====
    advice = (
        res.get("choices", [{}])[0]
        .get("message", {})
        .get("content")
    )

    if not advice:
        advice = str(res)

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

if __name__ == "__main__":
    run_agent()
