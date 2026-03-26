import pvporcupine
import pyaudio
import struct
import os

def listen_wake_word():

    access_key = "YOUR_ACCESS_KEY"

    base_path = os.path.dirname(os.path.abspath(__file__))

    keyword_path = "/Users/ravikantpandit/Desktop/Shiva-main/engine/madhav_en_mac_v4_0_0.ppn"

    print("Loading keyword from:", keyword_path)
    print("Exists:", os.path.exists(keyword_path))

    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=[keyword_path]
    )

    pa = pyaudio.PyAudio()

    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Listening for wake word...")

    while True:
        pcm = stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print("Wake word detected!")
            return True