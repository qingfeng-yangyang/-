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

    # ===== 天气 API =====
    url = "https://api.open-meteo.com/v1/forecast?latitude=23.12&longitude=114.41&current=temperature_2m,wind_speed_10m,precipitation"
    data = requests.get(url).json()

    temp = data["current"]["temperature_2m"]
    wind = data["current"]["wind_speed_10m"]
    rain = data["current"]["precipitation"]

    # ===== Prompt =====
    prompt = f"""
你是一个生活助手，请根据天气给出出行建议（中文简洁）：

温度：{temp}
风速：{wind}
降雨：{rain}

要求：
- 是否适合出门
- 是否需要带伞
- 一句总结
"""

    # ===== 豆包 EP 请求 =====
    try:
        response = requests.post(
            f"https://ark.cn-beijing.volces.com/api/v3/{endpoint}/chat/completions",
            headers={
                "Authorization": f"Bearer {ark_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "Doubao-Seed-2.0-lite",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            },
            timeout=20
        )

        print("STATUS:", response.status_code)
        print("TEXT:", response.text)

        res = response.json()

        # ===== 安全解析 =====
        if "choices" in res and len(res["choices"]) > 0:
            advice = res["choices"][0]["message"]["content"]
        else:
            advice = "AI返回异常：" + str(res)

    except Exception as e:
        advice = f"请求失败：{str(e)}"

    # ===== 邮件 =====
    msg = MIMEText(advice, "plain", "utf-8")
    msg["Subject"] = "今日AI天气建议"
    msg["From"] = email
    msg["To"] = email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, app_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print("EMAIL ERROR:", str(e))

    print("AGENT RUN SUCCESS")

if __name__ == "__main__":
    run_agent()
