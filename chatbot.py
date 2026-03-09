
from openai import OpenAI
import os

client = OpenAI(api_key="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")

print("AI Chatbot (type 'exit' to quit)")

messages = []

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    reply = response.choices[0].message.content
    print("Bot:", reply)

    messages.append({"role": "assistant", "content": reply})