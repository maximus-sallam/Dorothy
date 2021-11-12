# Dorothy integrated AI / speech-to-text / text-to-speech / mouth articulation

# Import necessary libraries.

# The Natural Language Toolkit (NLTK) is a Python package for natural
# language processing.
# https://pypi.org/project/nltk/
import nltk
from nltk.stem import WordNetLemmatizer

# Python Serial Port Extension for Win32, OSX, Linux, BSD, Jython, IronPython.
# https://pypi.org/project/pyserial/
import serial

# This module provides various time-related functions.
# https://docs.python.org/3/library/time.html
import time

# This module provides a portable way of using operating system
# dependent functionality.
# https://docs.python.org/3/library/os.html
import os

# Cloud Text-to-Speech API: Synthesizes natural-sounding speech by applying
# powerful neural network models.
# https://pypi.org/project/google-cloud-texttospeech/
from google.cloud import texttospeech

# The built-in string class provides the ability to do complex variable
# substitutions and value formatting via the format() method described in
# PEP 3101. The Formatter class in the string module allows you to create and
# customize your own string formatting behaviors using the same implementation
# as the built-in format() method.
# https://docs.python.org/3/library/string.html
import string

# Manipulate audio with an simple and easy high level interface.
# Pydub lets you do stuff to audio in a way that isn't stupid.
# https://pypi.org/project/pydub/
from pydub import AudioSegment

# pygame is a free and open-source cross-platform library for the development
# of multimedia applications like video games using Python. It uses the Simple
# DirectMedia Layer library and several other popular libraries to abstract
# the most common functions, making writing these programs a more intuitive task.
# This module contains classes for loading Sound objects and controlling playback.
# The mixer module is optional and depends on SDL_mixer. Your program should test
# that pygame.mixerpygame module for loading and playing sounds is available and
# initialized before using it.
# https://pypi.org/project/pygame/
# http://www.pygame.org/docs/ref/mixer.html
from pygame import mixer

# Manipulate audio with an simple and easy high level interface.
# Pydub lets you do stuff to audio in a way that isn't stupid.
# This module simply exposes a wrapper of a pydub.AudioSegment object.
# https://pypi.org/project/pydub/
# https://audiosegment.readthedocs.io/en/latest/audiosegment.html
from pydub import AudioSegment

# Library for performing speech recognition, with support for several engines
# and APIs, online and offline.
# https://pypi.org/project/SpeechRecognition/
import speech_recognition

# This Python module provides bindings for the PortAudio library and a few
# convenience functions to play and record NumPy arrays containing audio signals.
# https://pypi.org/project/sounddevice/
import sounddevice

# Writes a simple uncompressed WAV file. To write multiple-channels, use a 2-D
# array of shape (Nsamples, Nchannels).
# The bits-per-sample and PCM/float will be determined by the data-type.
# https://pypi.org/project/scipy/
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html
from scipy.io.wavfile import write

# This module implements pseudo-random number generators for various distributions.
# https://docs.python.org/3/library/random.html
import random

# A set of python modules for machine learning and data mining.
# https://pypi.org/project/sklearn/
from sklearn.feature_extraction.text import TfidfVectorizer as tfidf_vectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Warning messages are typically issued in situations where it is useful to
# alert the user of some condition in a program, where that condition (normally)
# doesn’t warrant raising an exception and terminating the program.
# https://docs.python.org/3/library/warnings.html
import warnings

warnings.filterwarnings("ignore")

# For downloading packages.
nltk.download("popular", quiet=True)

# Uncomment the following only the first time.
# nltk.download("punkt") # First-time use only.
# nltk.download("wordnet") # First-time use only.

# Reading in the corpus.
with open("chatbot.txt", "r",
          encoding="utf8",
          errors="ignore") as fin:
    raw = fin.read().lower()

# Tokenization.
sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
word_tokens = nltk.word_tokenize(raw)  # converts to list of words

# Preprocessing.
lemmer = WordNetLemmatizer()

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
# serial_port = serial.Serial("COM7", 9600)


def lem_tokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punctuation_dict = dict((ord(punctuation), None) for punctuation in string.punctuation)


def lem_normalize(text):
    return lem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_dict)))


# Keyword Matching.
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]


def greeting(sentence):
    # If user's input is a greeting, return a greeting response.
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Generating response.
def response(response_from_user):
    dorothy_response = ""
    sent_tokens.append(response_from_user)
    tfidf_vector = tfidf_vectorizer(tokenizer=lem_normalize,
                                    stop_words="english")
    tfidf = tfidf_vector.fit_transform(sent_tokens)
    values = cosine_similarity(tfidf[-1], tfidf)
    idx = values.argsort()[0][-2]
    flat = values.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if req_tfidf == 0:
        dorothy_response = dorothy_response + "I am sorry! I don't understand you"
        return dorothy_response
    else:
        dorothy_response = dorothy_response + sent_tokens[idx]
        return dorothy_response


# Google Wavenet API credentials file.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "text-to-speech-278712-83ab5ff5f64a.json"

# Instantiates a client.
client = texttospeech.TextToSpeechClient()

# Recognize speech input from the microphone.
recognizer = speech_recognition.Recognizer()

# Build the voice request, select language code ("en-US")
# and the ssml voice gender ("female").
voice = texttospeech.VoiceSelectionParams(language_code="en-US",
                                          name="en-US-Wavenet-F",
                                          ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)

# Selects the type of audio file to return.
audio_config = texttospeech.AudioConfig(speaking_rate=1,
                                        audio_encoding=texttospeech.AudioEncoding.MP3)

# Dorothy introduces herself.
intro = "My name is Dorothy. I will answer your questions about chatbots. If you want to exit, say Bye!"
synthesis_input = texttospeech.SynthesisInput(text=intro)


# Sample rate.
fs = 44100
# Duration of recording.
seconds = 3

# Records users voice.
print("Recording...")
my_recording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
sounddevice.wait()  # Wait until recording is finished
write("mic_recording.rwav", fs, my_recording)  # Save as WAV file
print("Recording finished.")

# Converts raw wave file into readable wave file.
sound = AudioSegment.from_wav("mic_recording.rwav")
sound.export("mic_recording.wav", format="wav")

# Sets to converted wave file to the audio source.
microphone = speech_recognition.AudioFile("mic_recording.wav")
with microphone as source:
    audio = recognizer.record(source)

# Listens for an input sentence.
your_sentence = recognizer.recognize_google(audio)
response = client_synthesize_speech()

# Takes an input sentence.
#        your_sentence = input("Enter your sentence:")

# Test speech - For adjusting servo settings. Comment this out in production.
#        your_sentence = "Hello. My name is Dorothy. I am a robot and I am here to help you succeed."

# Set the text input to be synthesized.
synthesis_input = texttospeech.SynthesisInput(text=your_sentence)

# Separates the input sentence into a list, converts all characters to lowercase, and strips away punctuation.
#        your_sentence = your_sentence.lower().translate(str.maketrans("", "", string.punctuation))
#        your_sentence = your_sentence.split()
#        print(recognizer.recognize_google(audio))
#        print("Articulating Arduino:", your_sentence)

# Finds an ARPAbet translation of each word in the sentence and stores it in the result array.
#        result = []
#        for words in your_sentence:
#            result.append(arpabet[words])
#        array_length = len(result)

# Prints each phoneme separated by a "."
#        for x in range(0, array_length):
#            word_length = len(result[x][0])
#            for y in range(0, word_length):
#                print(result[x][0][y], end="")
#                serial_port.write(result[x][0][y].encode())
#                print(".", end="")
#                serial_port.write(".".encode())
#        print("$", end="")

#        # Writes each phoneme to the Arduino COM port.
#        serial_port.write("$".encode())
#        print(" wrote to Arduino.")

# Writes the synthetic audio to the output file.
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)

# Plays the synthetic audio.
mixer.init()
mixer.music.load("output.mp3")
mixer.music.play()

# Waits for audio to finish playing and stops the audio.
while mixer.music.get_busy():
    time.sleep(1)
mixer.music.stop()

# Unloads the synthetic audio from resource allocation.
mixer.music.unload()

# Deletes the created audio file.
os.remove("mic_recording.rwav")
os.remove("mic_recording.wav")
os.remove("output.mp3")

#    except KeyError:
#        print("An error has occurred. Try again.")
#        continue
