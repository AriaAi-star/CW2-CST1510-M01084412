from openai import OpenAI

client = OpenAI(
    api_key="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"
)

# Fixed: Use chat.completions instead of responses
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Fixed: gpt-5-nano doesn't exist
    messages=[
        {"role": "user", "content": "write a haiku about ai"}
    ]
)

print(response.choices[0].message.content)
