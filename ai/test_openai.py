from openai import OpenAI

# 实例化客户端
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=""
)
response = client.responses.create(
    model="openai/gpt-oss-20b:free",
    input=""
)

print(response)