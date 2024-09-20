from django.conf import settings
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_chat(question):
    """
    Generate a chat response based on the user's question.
    """
    system_prompt = set_system_prompt()
    user_prompt = set_user_prompt(question)
    messages = [
        system_prompt,
        user_prompt
    ]
    response = complete_chat(messages)
    return format_response(response)


def set_system_prompt():
    """
    Set the system prompt for the chat.
    """
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
    """
    Set the user prompt for the chat.
    """
    user_prompt = ""
    user_prompt = f"Question: {question}"
    return {
        "role": "user",
        "content": user_prompt
    }


def complete_chat(messages):
    """
    Configure and complete the chat.
    """
    return client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=100
    )


def format_response(response):
    """
    Format the chat response before returning it.
    """
    return response.choices[0].message.content.strip()
