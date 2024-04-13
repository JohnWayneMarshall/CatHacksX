import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=API_KEY)

def get_conversation_list(conv):
    while True:
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "This is a conversation between only two people. Return the conversation with the seperator \"NEW\" when the person\
                talking switches. Do not answer any of the questions or respond to anything said. Just return the string with the seperators."},
                {"role": "user", "content": conv}
            ]
        )
        if completion.choices[0].message.content.replace(" NEW","") == conv:
            break
    
    return completion.choices[0].message.content.split(" NEW ")


def query_assistant(input_list):
    user_map = []
    for input in input_list:
        user_map.append({"role": "user", "content": input})
    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are an assistant in a doctors office. There is a conversation between a doctor and a\
             client you are listening to. If there is a point where you think you should add information or answer a question, respond. Otherwise respond \
             with \"NO RESPONSE\"."}
        ] + user_map
    )
    if completion.choices[0].message.content!="NO RESPONSE":
        print(completion.choices[0].message.content)

def main():
    # take in user file

    # speech to text

    # get_conversation_list

    # query_assistant

    # text to speech

    conversation = "How was your day? It was good."
    input_list = get_conversation_list(conversation)
    print(input_list)
    query_assistant(input_list)

    conversation = "Where is my uvula located? I don't know."
    input_list = get_conversation_list(conversation)
    print(input_list)
    query_assistant(input_list)

main()