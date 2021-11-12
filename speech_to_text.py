# Speech-to-text / text-to-speech

# Import necessary libraries.

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
# games using Python. It uses the Simple DirectMedia Layer library and several other popular libraries to abstract
# the most common functions, making writing these programs a more intuitive task.
# This module contains classes for loading Sound objects and controlling playback. The mixer module is optional and
# depends on SDL_mixer. Your program should test that pygame.mixerpygame module for loading and playing sounds is
# available and initialized before using it.
# https://pypi.org/project/pygame/
# http://www.pygame.org/docs/ref/mixer.html
from pygame import mixer

# Manipulate audio with an simple and easy high level interface.
# Pydub lets you do stuff to audio in a way that isn't stupid.
# This module simply exposes a wrapper of a pydub.AudioSegment object.
# https://pypi.org/project/pydub/
# https://audiosegment.readthedocs.io/en/latest/audiosegment.html
from pydub import AudioSegment

# Library for performing speech recognition, with support for several engines and APIs, online and offline.
# https://pypi.org/project/SpeechRecognition/
import speech_recognition

# This Python module provides bindings for the PortAudio library and a few convenience functions to play and
# record NumPy arrays containing audio signals.
# https://pypi.org/project/sounddevice/
import sounddevice

# Writes a simple uncompressed WAV file. To write multiple-channels, use a 2-D array of shape (Nsamples, Nchannels).
# The bits-per-sample and PCM/float will be determined by the data-type.
# https://pypi.org/project/scipy/
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html
from scipy.io.wavfile import write


# Sample rate.
fs = 44100
# Duration of recording.
seconds = 5


print("Recording...")
my_recording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
sounddevice.wait()  # Wait until recording is finished
write("mic_test.rwav", fs, my_recording)  # Save as WAV file
print("Recording finished.")

sound = AudioSegment.from_wav("mic_test.rwav")
sound.export("mic_test.wav", format="wav")

recognizer = speech_recognition.Recognizer()

microphone = speech_recognition.AudioFile("mic_test.wav")
with microphone as source:
    audio = recognizer.record(source)

# Google Wavenet API credentials file.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "text-to-speech-278712-83ab5ff5f64a.json"

# Instantiates a client.
client = texttospeech.TextToSpeechClient()

print(recognizer.recognize_google(audio))
your_sentence = recognizer.recognize_google(audio)

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

# Deletes the created audio files.
os.remove("mic_test.rwav")
os.remove("mic_test.wav")
os.remove("test.mp3")
