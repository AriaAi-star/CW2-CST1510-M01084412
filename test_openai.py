from openai import OpenAI

client = OpenAI(
    api_key="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"
)

# Test OpenAI API
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "write a haiku about ai"}
    ]
)

print(response.choices[0].message.content)
