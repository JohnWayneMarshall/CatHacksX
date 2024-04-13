import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv('AI_API_KEY')

client = OpenAI(api_key=API_KEY)

completion = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": "You are an assistant in a doctors office. There is a conversation between a doctor and a\
         client you are listening to. If there is a point where you think you should add information or answer a question, respond. Otherwise respond \
         with \"NO RESPONSE\"."},
        {"role": "user", "content": "How was your day?"},
        {"role": "user", "content": "It was good."}
    ]
)

print(completion.choices[0].message.content)

completion = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": "You are an assistant in a doctors office. There is a conversation between a doctor and a\
         client you are listening to. If there is a point where you think you should add information or answer a question, respond. Otherwise respond \
         with \"NO RESPONSE\"."},
        {"role": "user", "content": "Where is my uvula located?"},
        {"role": "user", "content": "I don't know"}
    ]
)

print(completion.choices[0].message.content)