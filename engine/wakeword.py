import pvporcupine
import pyaudio
import struct


def listen_wake_word():

    porcupine = pvporcupine.create(
        access_key="+ZhgZ7Sk7VwpyVIE0quh7gpbzYdbXgBOVzydO1ZaazhAJdNpTd8AIA==",

        # default wake words
        # keywords=["jarvis", "computer"],

        # custom wake word
        keyword_paths=["engine/madhav_en_mac_0_0.ppn"]
    )

    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Listening for wake words...")

    while True:

        pcm = audio_stream.read(porcupine.frame_length)

        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:

            print("Wake word detected")

            return True