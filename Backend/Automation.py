from AppOpener import close , open as appopen
from webbrowser import open as webopen
from pywhatkit import search , playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os


env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

classes = {
    "clubm", 
    "Bgkfc", 
    "ITK00", 
    "'97fzt'", 
    "20lcc", 
    "gsrt vk bk fzv85b 'wdhmt'", 
    "pclugc", 
    "tw Data-text tw-text-small tw-ta",
    "12crac", 
    "0oWbd LTb05", 
    "u1v2d", 
    "webanewers-webanewers_table__webanewers-table", 
    "dboHo M6ddb gsrt", 
    "5klabd",
    "Lkkftc", 
    "v0Fsg", 
    "qv3Mpc", 
    "knc-reSec", 
    "SPZz6b"
}

useragent = 'Mozilla/5.0 (Windows NT 10.6; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.8.4896.75 Safari/537.36'

client = Groq(api_key=GroqAPIKey)

professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask."
]

messages = []

SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like lette"}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):

    def OpenNotpad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])

    def ContentWriterAI(prompt):
        messages.append({"role" : "user" , "content" :  f"{prompt}"}) 

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if hasattr(chunk.choices[0], "delta") and hasattr(chunk.choices[0].delta, "content"):
                content_piece = chunk.choices[0].delta.content
                if content_piece is not None:
                    Answer += content_piece

        Answer = Answer.replace("</s>" , "")
        messages.append({"role": "assistant" , "content": Answer})
        return Answer
    
    Topic = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    with open(rf"Data\{Topic.lower().replace(' ' , ' ')}.text" , "w", encoding="utf-8") as file:
        file.write(ContentByAI)

    OpenNotpad(rf"Data\{Topic.lower().replace(' ' , ' ')}.text")
    return True


def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True


def OpenApp(app , sess=requests.Session()):
    try:
        appopen(app , match_closest=True, output=True , throw_error=True)

    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html , 'html.parser')
            links = soup.find_all('a' , {'jsname':'UWckNb'})
            return [link.get('href') for link in links]
        
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent" : useragent}
            response = sess.get(url, headers=headers)

            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrieve search results")
                return None
        
        html = search_google(app)

        if html:
            links = extract_links(html)
            if links:
                webopen(links[0])

        return True
        
def CloseApp(app):

    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False
        

def System(command):

    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume unmute")

    def volume_up():
        keyboard.press_and_release("volume up")

    def volume_down():
        keyboard.press_and_release("volume down")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

async def TranslaterAndExecute(commands: list[str]):
    funcs = []

    for command in commands:

        if command.startswith("open "):
            if "open it" in command:
                pass

            if "open file" == command:
                pass

            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)

        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass

        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)
        
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content"))
            funcs.append(fun)

        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search  "))
            funcs.append(fun)

        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)

        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)

        else:
            print(f"no Function found. for {command}")

    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):

    async for result in TranslaterAndExecute(commands):
        pass
    return True

if __name__ == "__main__":
    asyncio.run(Automation([]))