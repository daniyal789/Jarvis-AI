from random import choice
from time import strftime

import speech_recognition as sr
import os
import webbrowser
import datetime
import openai
import random
import string
import groq
from groq import Groq
from config import apikey

chatStr=""
def chat(query):
    global chatStr
    # Initialize the Groq client with your API key
    client = Groq(api_key=apikey)
    # Create a chat completion request
    chatStr=f"Daniyal:{query}\n Jarvis:"
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content":chatStr
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    response_text = ""
    # Stream the completion result
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""

    chatStr += f"{response_text}\n"  # Update chat history
    say(response_text)  # Speak the entire response at once

    return response_text

def ai(prompt):
    # Initialize the Groq client with your API key
    client = Groq(api_key=apikey)
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    # Create a chat completion request
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Stream the completion result
    for chunk in completion:
        # print(chunk.choices[0].delta.content or "", end="")
        text+=chunk.choices[0].delta.content or ""

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

        # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def passgenerator():
    s1 = string.ascii_lowercase
    s2 = string.ascii_uppercase
    s3 = string.digits
    s4 = string.punctuation

    passlen = int(input("Enter the length of password: "))
    if (passlen < 8):
        print("Password length should be greater than 8")
        say("Password length should be greater than 8")
        say("Please try again")
        passgenerator()

    s = []
    s.extend(list(s1))
    s.extend(list(s2))
    s.extend(list(s3))
    s.extend(list(s4))

    random.shuffle(s)
    newpass = ("".join(s[0:passlen]))
    say("Here is your password")
    print()
    print(newpass)
    print()

def flip():
    say("Okay Sir, flipping a coin")
    coin = ['Heads', 'Tails']
    toss = random.choice(coin)
    say(f"I flipped a coin and its {toss}")


def rollDice():
    say("Okay Sir, rolling a dice")
    dice = ['1', '2', '3', '4', '5', '6']
    num = random.choice(dice)
    say(f"I rolled a dice and its {num}")


def say(text):
    # Escape single quotes in the text for PowerShell command
    text = text.replace("'", "''")
    os.system(f'powershell -Command "Add-Type –AssemblyName System.speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\');"')

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")  # Switched back to the standard Google recognizer
            print(f"User said: {query}")
            return query
        except Exception as e:
            print(e)
            return "Some Error Occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I")
    while True:
        print("Listening...")
        query = takecommand()
        sites=[["youtube","https://www.youtube.com/"],["wikipedia", "https://www.wikipedia.com"],["google","https://www.google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"opening {site[0]} sir....")
                webbrowser.open(site[1])
        songs=[["dekhte dekhte","C:/Users/daniy/Downloads/Dekhte Dekhte.mp3"],["yah tune", "D:/web/spotify clone/song/arijit/Ye Tune Kya Kiya-arijit.mp3"],["arijit","D:web/spotify clone/song/arijit/Ve Kamleya-arijit.mp3"],]
        for music in songs:
            if f"play {music[0]}".lower() in query.lower():
                say(f"playing {music[0]} sir.....")
                os.startfile(music[1])

        if "the time" in query:
            strfTime=datetime.datetime.now().strftime("%H,%M,%S")
            say(f"Sir the time is{strfTime}")
        apps = [["vs code", "C:/Users/daniy/OneDrive/Desktop/Visual Studio Code.lnk"],]
        for app in apps:
            if f"Open {app[0]}".lower() in query.lower():
                say(f"opening {app[0]} sir....")
                os.startfile(app[1])
        if "generate password" in query:
            passgenerator()

        elif ('flip a coin' in query) or ('flip coin' in query):
            flip()

        elif ('roll a dice' in query) or ('roll dice' in query):
            rollDice()
        elif "using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
        elif "Jarvis quit".lower() in query.lower():
            exit()
        elif "Jarvis reset chat".lower() in query.lower():
            chatStr=""
        else:
            chat(query)

