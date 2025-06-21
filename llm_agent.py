from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",  # LM Studio server
    api_key="lm-studio"  # фиктивный ключ (требуется по синтаксису OpenAI API)
)
print(1)
response = client.chat.completions.create(
    model="local-model",  # имя может быть фиктивным, главное — передать его
    messages=[
        {"role": "user", "content": "Привет! Расскажи, как работает LM Studio с Python?"}
    ],
    temperature=0.7
)
print(2)
print(response.choices[0].message.content)