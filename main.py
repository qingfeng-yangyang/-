import os
from openai import OpenAI

# 读取 GitHub Secrets
api_key = os.environ["ARK_API_KEY"]

# 创建客户端
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=api_key,
)

# 调用 AI
response = client.responses.create(
    model="ep-20260628222322-mstpq",
    input="你好，请介绍一下你自己。"
)

# 打印完整返回
print("===== AI RESPONSE =====")
print(response)
print("=======================")
