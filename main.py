import os
import requests
import smtplib
from email.mime.text import MIMEText
from openai import OpenAI


def run_agent():

    # ===== Secrets =====
    email = os.environ["EMAIL"]
    app_password = os.environ["APP_PASSWORD"]
    ark_key = os.environ["ARK_API_KEY"]

    # ===== 天气 =====
    weather = requests.get(
        "https://api.open-meteo.com/v1/forecast?latitude=23.12&longitude=114.41&current=temperature_2m,wind_speed_10m,precipitation"
    ).json()

    temp = weather["current"]["temperature_2m"]
    wind = weather["current"]["wind_speed_10m"]
    rain = weather["current"]["precipitation"]

    # ===== AI =====
    client = OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=ark_key,
    )

    prompt = f"""
你是一个生活助手，请根据下面天气给出建议。

天气：
温度：{temp}℃
风速：{wind} m/s
降雨：{rain} mm

请回答：

1. 今天是否适合出门
2. 是否建议带伞
3. 穿衣建议
4. 一句话总结

回答尽量简洁。
"""

    try:
        response = client.responses.create(
            model="ep-20260628222322-mstpq",
            input=prompt
        )

        advice = response.output[1].content[0].text

    except Exception as e:
        advice = f"AI调用失败：{e}"

    # ===== 邮件内容 =====
    body = f"""
🌤 今日天气

温度：{temp} ℃
风速：{wind} m/s
降雨：{rain} mm


🤖 豆包建议

{advice}
"""

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = "今日AI天气助手"
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
