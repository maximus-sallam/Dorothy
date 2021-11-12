# ARPAbet text-to-speech / mouth articulation

# Import necessary libraries.

# The Natural Language Toolkit (NLTK) is a Python package for natural language processing.
# https://pypi.org/project/nltk/
import nltk

# Python Serial Port Extension for Win32, OSX, Linux, BSD, Jython, IronPython.
# https://pypi.org/project/pyserial/
import serial

# This module provides various time-related functions.
# https://docs.python.org/3/library/time.html
import time

# This module provides a portable way of using operating system dependent functionality.
# https://docs.python.org/3/library/os.html
import os

# pygame is a free and open-source cross-platform library for the development of multimedia applications like video
# games using Python. It uses the Simple DirectMedia Layer library and several other popular libraries to abstract the
# most common functions, making writing these programs a more intuitive task.
# https://pypi.org/project/pygame/
from pygame import mixer

# Cloud Text-to-Speech API: Synthesizes natural-sounding speech by applying powerful neural network models.
# https://pypi.org/project/google-cloud-texttospeech/
from google.cloud import texttospeech

# The built-in string class provides the ability to do complex variable substitutions and value formatting via the
# format() method described in PEP 3101. The Formatter class in the string module allows you to create and customize
# your own string formatting behaviors using the same implementation as the built-in format() method.
# https://docs.python.org/3/library/string.html
import string


# Google Wavenet API credentials file.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "text-to-speech-278712-83ab5ff5f64a.json"

# Instantiates a client.
client = texttospeech.TextToSpeechClient()

# The dictionary contains 127069 entries.  Of these, 119400 words are assigned
# a unique pronunciation, 6830 words have two pronunciations, and 839 words have
# three or more pronunciations.  Many of these are fast-speech variants.
# https://www.nltk.org/_modules/nltk/corpus/reader/cmudict.html
arpabet = nltk.corpus.cmudict.dict()

# Change this to the port your Arduino is connected to.
serial_port = serial.Serial("COM3", 9600)

while True:
    try:
        # Takes an input sentence.
        # your_sentence = input("Enter your sentence:")
        # Test speech - For adjusting servo settings. Comment this out in production.
        your_sentence = "Hello. My name is Dorothy. I would like to get to know you."

        # Set the text input to be synthesized.
        synthesis_input = texttospeech.SynthesisInput(text=your_sentence)

        # Build the voice request, select language code ("en-US") and the ssml voice gender ("female").
        voice = texttospeech.VoiceSelectionParams(language_code="en-US",
                                                  name="en-US-Wavenet-F",
                                                  ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)

        # Selects the type of audio file to return.
        audio_config = texttospeech.AudioConfig(speaking_rate=1,
                                                audio_encoding=texttospeech.AudioEncoding.MP3)

        # Performs the text-to-speech request on the text input with the selected voice parameters and audio file type.
        response = client.synthesize_speech(input=synthesis_input,
                                            voice=voice,
                                            audio_config=audio_config)

        # Writes the synthetic audio to the output file.
        with open("output.mp3", "wb") as out:
            out.write(response.audio_content)

        #  Separates the input sentence into a list, converts all characters to lowercase, and strips away punctuation.
        your_sentence = your_sentence.lower().translate(str.maketrans("", "", string.punctuation))
        your_sentence = your_sentence.split()
        print("You Typed:", your_sentence)

        # Finds an ARPAbet translation of each word in the sentence and stores it in the result array.
        result = []
        for words in your_sentence:
            result.append(arpabet[words])
        array_length = len(result)

        # Plays the synthetic audio.
        mixer.init()
        mixer.music.load("output.mp3")
        mixer.music.play()

        # Prints each phoneme separated by a "."
        for x in range(0, array_length):
            word_length = len(result[x][0])
            for y in range(0, word_length):
                print(result[x][0][y], end="")

                # Sets the rate at which the mouth moves.
                time.sleep(0.0075)
                serial_port.write(result[x][0][y].encode())
                print(".", end="")
                serial_port.write(".".encode())
        print("$", end="")

        # Writes each phoneme to the Arduino COM port.
        serial_port.write("$".encode())
        print(" wrote to Arduino.")

        # Waits for audio to finish playing and stops the audio.
        while mixer.music.get_busy():
            time.sleep(1)
        mixer.music.stop()

        # Unloads the synthetic audio from resource allocation.
        mixer.music.unload()

        # Deletes the created audio file.
        os.remove("output.mp3")
        break

    except KeyError:
        print("An error has occurred. Try again.")
        continue
