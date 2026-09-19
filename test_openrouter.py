import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

response = client.chat.completions.create(
    model=os.getenv("OPENROUTER_MODEL"),
    messages=[
        {
            "role": "user",
            "content": "Classify this sentence as toxic or non-toxic: I love this course."
        }
    ],
)

print(response.choices[0].message.content)