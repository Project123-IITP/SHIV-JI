import speech_recognition as sr
import asyncio
import edge_tts
import os
from playsound import playsound
from langdetect import detect


VOICE_EN = "en-IN-PrabhatNeural"
VOICE_HI = "hi-IN-MadhurNeural"


def detect_voice(text):

    try:
        lang = detect(text)

        if lang == "hi":
            return VOICE_HI
        else:
            return VOICE_EN

    except:
        return VOICE_EN


async def speak_async(text, voice):

    communicate = edge_tts.Communicate(text, voice)

    await communicate.save("voice.mp3")


def speak(text):

    text = str(text)

    print("Maadhav:", text)

    voice = detect_voice(text)

    if os.path.exists("voice.mp3"):
        os.remove("voice.mp3")

    asyncio.run(speak_async(text, voice))

    playsound("voice.mp3")


def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        r.pause_threshold = 1

        r.adjust_for_ambient_noise(source)

        audio = r.listen(source)

    try:

        query = r.recognize_google(audio, language="en-IN")

        print("User:", query)

        return query.lower()

    except:

        return ""