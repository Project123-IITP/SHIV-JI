import speech_recognition as sr
import eel
import asyncio
import edge_tts
from playsound import playsound


# -------- VOICE SETTINGS --------

VOICE = "en-US-AriaNeural"  # Siri like Indian female voice


# -------- SPEAK FUNCTION --------

async def speak_async(text):

    communicate = edge_tts.Communicate(text, VOICE)

    await communicate.save("voice.mp3")


def speak(text):

    text = str(text)

    print("Maadhav:", text)

    # UI display
    try:
        eel.DisplayMessage(text)
        eel.receiverText(text)
    except:
        pass

    asyncio.run(speak_async(text))

    playsound("voice.mp3")


# -------- TAKE COMMAND --------

def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        try:
            eel.DisplayMessage("Listening...")
        except:
            pass

        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source)

    try:

        print("Recognizing...")

        query = r.recognize_google(audio, language="en-in")

        print("User said:", query)

        try:
            eel.DisplayMessage(query)
        except:
            pass

    except Exception as e:

        print("Say that again please...")

        return ""

    return query.lower()


# -------- MAIN COMMAND SYSTEM --------

@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
    else:
        query = message.lower()

    print("User:", query)

    if query == "":
        return

    try:

        from engine.features import assistantBrain

        assistantBrain(query)

    except Exception as e:

        print("Assistant Error:", e)

        speak("Sorry Ravikant, something went wrong")

    try:
        eel.ShowHood()
    except:
        pass