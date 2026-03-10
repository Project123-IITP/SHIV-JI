import os
import eel

from engine.features import *
from engine.command import *
from engine.auth import recoganize
from engine.wakeword import listen_wake_word


def start():

    print("Shiv starting...")

    eel.init("www")

    playAssistantSound()

    @eel.expose
    def init():

        eel.hideLoader()

        speak("Ready for Face Authentication")

        # Face Authentication
        flag = recoganize.AuthenticateFace()

        if flag == 1:

            eel.hideFaceAuth()

            speak("Face Authentication Successful")

            eel.hideFaceAuthSuccess()

            speak("Hello Ravikant, I am Maadhav")

            eel.hideStart()

            playAssistantSound()

            # Wake word system
            speak("Say Hey Maadhav to activate me")

            while True:

                if listen_wake_word():

                    speak("Yes Ravikant")

                    startExecution()

        else:

            speak("Face Authentication Failed")

            print("Access Denied")

            os._exit(0)

    # Mac Chrome open
    os.system('open -a "Google Chrome" http://localhost:8000/index.html')

    eel.start(
        'index.html',
        size=(1000, 600),
        host='localhost',
        port=8000
    )


if __name__ == "__main__":
    start()