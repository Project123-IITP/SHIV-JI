import os
import sqlite3
import webbrowser
import eel
import pywhatkit as kit
import speech_recognition as sr

from engine.command import speak
from engine.config import ASSISTANT_NAME
from engine.helper import extract_yt_term

import google.generativeai as genai


# ---------------- DATABASE ----------------

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()


# ---------------- START SOUND ----------------

@eel.expose
def playAssistantSound():
    from playsound import playsound
    playsound("www/assets/audio/start_sound.mp3")


# ---------------- OPEN APPS ----------------

def openCommand(query):

    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")

    app_name = query.strip().lower()

    if app_name == "":
        return

    try:

        # check system apps
        cursor.execute(
            "SELECT path FROM sys_command WHERE name=?",
            (app_name,)
        )

        result = cursor.fetchone()

        if result:

            speak("Opening " + app_name)

            os.system(f'open "{result[0]}"')

            return

        # check web commands
        cursor.execute(
            "SELECT url FROM web_command WHERE name=?",
            (app_name,)
        )

        result = cursor.fetchone()

        if result:

            speak("Opening " + app_name)

            webbrowser.open(result[0])

            return

        speak("Application not found")

    except Exception as e:

        print("Open command error:", e)

        speak("Something went wrong")


# ---------------- YOUTUBE ----------------

def PlayYoutube(query):

    search_term = extract_yt_term(query)

    if search_term == "":
        speak("What should I play?")
        return

    speak("Playing " + search_term + " on YouTube")

    kit.playonyt(search_term)


# ---------------- GEMINI AI ----------------

genai.configure(api_key="AIzaSyCYOpuyL5Mt9ccUo6CL0yMNV_BbWCNBoHw")

model = genai.GenerativeModel("gemini-1.5-flash")


def chatBot(query):

    try:

        response = model.generate_content(query)

        answer = response.text

        print("AI:", answer)

        speak(answer)

        return answer

    except Exception as e:

        print("AI Error:", e)

        speak("I could not connect to AI right now")


# ---------------- ASSISTANT BRAIN ----------------

def assistantBrain(query):

    query = query.lower()

    print("User:", query)

    # ---------- OPEN WEBSITES ----------

    if "open youtube" in query:

        webbrowser.open("https://youtube.com")

        speak("Opening YouTube")

    elif "open google" in query:

        webbrowser.open("https://google.com")

        speak("Opening Google")

    elif "open whatsapp" in query:

        webbrowser.open("https://web.whatsapp.com")

        speak("Opening WhatsApp")

    elif "open instagram" in query:

        webbrowser.open("https://instagram.com")

        speak("Opening Instagram")

    # ---------- PLAY MUSIC ----------

    elif "play" in query:

        PlayYoutube(query)

    # ---------- GENERAL AI ----------

    else:

        chatBot(query)


# ---------------- VOICE INPUT ----------------

def takeCommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        r.pause_threshold = 1

        r.adjust_for_ambient_noise(source)

        audio = r.listen(source)

    try:

        print("Recognizing...")

        query = r.recognize_google(audio, language="en-in")

        print("User said:", query)

        return query.lower()

    except Exception as e:

        print("Voice error:", e)

        return ""


# ---------------- MAIN EXECUTION ----------------

def startExecution():

    while True:

        query = takeCommand()

        if query == "":
            continue

        print("User:", query)

        if "open" in query:

            openCommand(query)

        elif "play" in query:

            PlayYoutube(query)

        else:

            assistantBrain(query)