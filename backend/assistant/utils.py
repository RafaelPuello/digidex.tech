from django.conf import settings
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_chat(question):
    system_prompt = set_system_prompt()
    user_prompt = set_user_prompt(question)
    messages = [
        system_prompt,
        user_prompt
    ]

    response = complete_chat(messages)
    return format_response(response)


def set_system_prompt():
    sys_prompt = (
        "You are a helpful but not too formal assistant tasked with helping users with their questions about whatever they have in their inventory or party. "
        "Each user has their own inventory to store boxes and entities. "
        "You should provide helpful information and guidance to the user. "
        "You should answer in a manner that is concise. "
        "The user will ask you a question about their inventory, and you should provide a helpful response "
        "and clarify when the instructions are unclear.  Unless asked, do not repeat the user's username."
    )
    return {
        "role": "system",
        "content": sys_prompt
    }


def set_user_prompt(question):
    user_prompt = ""
    user_prompt = f"Question: {question}"
    return {
        "role": "user",
        "content": user_prompt
    }


def complete_chat(messages):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=100
    )
    return response


def format_response(response):
    chat = response.choices[0].message.content
    chat = chat.strip()
    return chat
