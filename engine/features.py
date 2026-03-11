import os
import webbrowser
import eel
import pywhatkit as kit
import speech_recognition as sr
import ollama

from langdetect import detect
from engine.command import speak
from engine.config import ASSISTANT_NAME
from engine.helper import extract_yt_term
from engine.memory import add_memory, get_memory


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

    if not app_name:
        return

    try:
        speak(f"Opening {app_name}")
        os.system(f"open -a '{app_name}'")

    except Exception as e:
        print("Open Error:", e)
        speak("Application not found")


# ---------------- YOUTUBE ----------------

def PlayYoutube(query):

    search_term = extract_yt_term(query)

    if not search_term:
        speak("What should I play?")
        return

    speak(f"Playing {search_term} on YouTube")
    kit.playonyt(search_term)


# ---------------- IMAGE ANALYSIS ----------------

@eel.expose
def analyzeImage(image_path):

    try:

        response = ollama.chat(
            model="llava",
            messages=[
                {
                    "role": "user",
                    "content": "Describe this image in detail",
                    "images": [image_path]
                }
            ]
        )

        answer = response["message"]["content"]

        print("Vision:", answer)

        speak(answer)

        return answer

    except Exception as e:

        print("Image AI Error:", e)

        speak("I could not analyze the image")


# ---------------- AI CHAT WITH MEMORY + LANGUAGE ----------------

def chatBot(query):

    try:

        # detect user language
        language = detect(query)

        # save user message
        add_memory("user", query)

        # load memory
        messages = get_memory()

        # add language instruction
        prompt = f"Answer in {language} language: {query}"

        messages.append({
            "role": "user",
            "content": prompt
        })

        response = ollama.chat(
            model="llama3",
            messages=messages
        )

        answer = response["message"]["content"]

        print("AI:", answer)

        # save AI reply
        add_memory("assistant", answer)

        speak(answer)

        return answer

    except Exception as e:

        print("Ollama Error:", e)

        speak("I could not connect to the AI model")


# ---------------- ASSISTANT BRAIN ----------------

def assistantBrain(query):

    query = query.lower()

    print("User:", query)

    try:

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

        elif "play" in query:
            PlayYoutube(query)

        elif "analyze image" in query or "describe image" in query:

            speak("Please enter the image path")

            image_path = input("Image path: ")

            if os.path.exists(image_path):
                analyzeImage(image_path)
            else:
                speak("Image file not found")

        else:
            chatBot(query)

    except Exception as e:

        print("Assistant Brain Error:", e)

        speak("Something went wrong")


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

    except sr.UnknownValueError:

        print("Could not understand")
        return ""

    except Exception as e:

        print("Voice Error:", e)
        return ""


# ---------------- MAIN EXECUTION ----------------

def startExecution():

    while True:

        query = takeCommand()

        if not query:
            continue

        print("User:", query)

        if "open" in query:
            openCommand(query)

        elif "play" in query:
            PlayYoutube(query)

        else:
            assistantBrain(query)