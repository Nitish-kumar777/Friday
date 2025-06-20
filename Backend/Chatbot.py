from groq import Groq
from json import load , dump
import datetime
from dotenv import dotenv_values
import os

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)
os.makedirs("Data", exist_ok=True)

messages = []
chat_log_path = os.path.join("Data", "ChatLog.json")

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [
    {"role": "system", "content": System},
]

try:
    if os.path.exists(chat_log_path) and os.path.getsize(chat_log_path) > 0:
        with open(chat_log_path, "r") as f:
            messages = load(f)
    else:
        with open(chat_log_path, "w") as f:
            dump([], f)
except Exception as e:
    print(f"Error loading chat log: {e}")
    messages = []
    with open(chat_log_path, "w") as f:
        dump([], f)

def RealtimeInformation():
    current_data_time = datetime.datetime.now()
    day = current_data_time.strftime("%A")
    date = current_data_time.strftime("%d")
    month = current_data_time.strftime("%B")
    year = current_data_time.strftime("%Y")
    hour = current_data_time.strftime("%H")
    minute = current_data_time.strftime("%M")
    second = current_data_time.strftime("%S")

    data = f"please use this real-time information if needed,\n"
    data += f"Current Date: {day}\nDate, {date}\nMonth {month}\nYear {year}\n"
    data += f"Time: {hour} hours : {minute} minutes : {second} seconds\n"
    return data

def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

def ChatBot(Query):
    try:
        # Load existing messages
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
        
        # If this is the first message, include the system prompt
        if not messages:
            messages = SystemChatBot.copy()
        
        # Add user message
        messages.append({"role": "user", "content": Query})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,  # Use the full conversation history
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "").strip()
        
        # Add assistant's response to history
        messages.append({"role": "assistant", "content": Answer})

        # Save updated conversation
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer=Answer)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        # If error occurs, save what we have
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)
        return "I encountered an error. Please try again."

   
if __name__ == "__main__":
    while True:
        user_input = input(f"{Username} >>> ")
        if user_input.lower() in ["exit", "bye", "quit"]:
            print(f"{Assistantname} >>> Goodbye!")
            break
        response = ChatBot(user_input)
        print(f"{Assistantname} >>> {response}") 