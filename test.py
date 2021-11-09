# This module provides a portable way of using operating system dependent functionality.
# https://docs.python.org/3/library/os.html
import os

# This module provides various time-related functions.
# https://docs.python.org/3/library/time.html
import time

# Cloud Text-to-Speech API: Synthesizes natural-sounding speech by applying powerful neural network models.
# https://pypi.org/project/google-cloud-texttospeech/
from google.cloud import texttospeech

# pygame is a free and open-source cross-platform library for the development of multimedia applications like video
# games using Python. It uses the Simple DirectMedia Layer library and several other popular libraries to abstract the
# most common functions, making writing these programs a more intuitive task.
# https://pypi.org/project/pygame/
from pygame import mixer

# Manipulate audio with an simple and easy high level interface.
# Pydub lets you do stuff to audio in a way that isn't stupid.
# https://pypi.org/project/pydub/
from pydub import AudioSegment


# Google Wavenet API credentials file.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "text-to-speech-278712-83ab5ff5f64a.json"

# Instantiates a client.
client = texttospeech.TextToSpeechClient()

your_sentence = "This is a test of the emergency alert system"

# Set the text input to be synthesized.
synthesis_input = texttospeech.SynthesisInput(text=your_sentence)

# Build the voice request, select language code ("en-US") and the ssml voice gender ("female").
voice = texttospeech.VoiceSelectionParams(language_code="en-US",
                                          name="en-US-Wavenet-F",
                                          ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)

# Selects the type of audio file to return.
audio_config = texttospeech.AudioConfig(speaking_rate=1.0,
                                        audio_encoding=texttospeech.AudioEncoding.MP3)

# Performs the text-to-speech request on the text input with the selected voice parameters and audio file type.
response = client.synthesize_speech(input=synthesis_input,
                                    voice=voice,
                                    audio_config=audio_config)

# Writes the synthetic audio to the output file.
with open("test.mp3", "wb") as out:
    out.write(response.audio_content)

# Plays the synthetic audio.
mixer.init()
mixer.music.load("test.mp3")
mixer.music.play()

# Waits for audio to finish playing and stops the audio.
while mixer.music.get_busy():
    time.sleep(1)
mixer.music.stop()

# Unloads the synthetic audio from resource allocation.
mixer.music.unload()

# Deletes the created audio file.
# os.remove("test.mp3")

sound = AudioSegment.from_mp3("test.mp3")
sound.export("test.wav", format="wav")

mixer.init()
mixer.music.load("test.wav")
mixer.music.play()

# Waits for audio to finish playing and stops the audio.
while mixer.music.get_busy():
    time.sleep(1)
mixer.music.stop()

# Unloads the synthetic audio from resource allocation.
mixer.music.unload()
