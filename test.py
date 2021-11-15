# ARPAbet text-to-speech / mouth articulation

# Import necessary libraries.

# Python Serial Port Extension for Win32, OSX, Linux, BSD, Jython, IronPython.
# https://pypi.org/project/pyserial/
import serial

# This module implements pseudo-random number generators for various distributions.
# https://docs.python.org/3/library/random.html
import random

# The built-in string class provides the ability to do complex variable
# substitutions and value formatting via the format() method described in
# PEP 3101. The Formatter class in the string module allows you to create and
# customize your own string formatting behaviors using the same implementation
# as the built-in format() method.
# https://docs.python.org/3/library/string.html
import string

# Warning messages are typically issued in situations where it is useful to
# alert the user of some condition in a program, where that condition (normally)
# doesn't warrant raising an exception and terminating the program.
# https://docs.python.org/3/library/warnings.html
import warnings

# A set of python modules for machine learning and data mining.
# https://pypi.org/project/sklearn/
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# The Natural Language Toolkit (NLTK) is a Python package for natural language processing.
# https://pypi.org/project/nltk/
import nltk
from nltk.stem import WordNetLemmatizer

# This module provides a portable way of using operating system dependent functionality.
# https://docs.python.org/3/library/os.html
import os

# This module provides various time-related functions.
# https://docs.python.org/3/library/time.html
import time

# This module provides access to Transport Layer Security (often known as “Secure Sockets Layer”)
# encryption and peer authentication facilities for network sockets, both client-side and server-side.
# https://docs.python.org/3/library/ssl.html
import ssl

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

# Writes a simple uncompressed WAV file. To write multiple-channels, use a 2-D array of shape (samples, channels).
# The bits-per-sample and PCM/float will be determined by the data-type.
# https://pypi.org/project/scipy/
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html
from scipy.io.wavfile import write

# Wikipedia is a Python library that makes it easy to access and parse data from Wikipedia.
# https://pypi.org/project/wikipedia/
import wikipedia

warnings.filterwarnings("ignore")

# For downloading packages on macOS.
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Downloads the NLTK popular library.
nltk.download("popular", quiet=True)

# First-time use only - Uncomment the following only the first time.
# nltk.download("punkt")
# nltk.download("wordnet")


# Reading in the corpus.
with open("chatbot.txt", "r",
          encoding="utf8",
          errors="ignore") as fin:
    raw = fin.read().lower()

# Tokenization - Converts to list of sentences.
sent_tokens = nltk.sent_tokenize(raw)

# converts to list of words
word_tokens = nltk.word_tokenize(raw)

# Preprocessing.
lemmer = WordNetLemmatizer()

# Google Wavenet API credentials file.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "text-to-speech-278712-83ab5ff5f64a.json"

# Introduction.
intro = "My name is Dorothy. I will answer your questions about artificial intelligence. If you want to stop, say Bye!"

# Keyword Matching.
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
GREETING_RESPONSES = ["fuck my ass", "hi", "hey", "howdy", "hi there",
                      "hello", "I'm glad you are talking to me", "how do you do"]

# Removes punctuation.
remove_punctuation_dict = dict((ord(punctuation), None) for punctuation in string.punctuation)

# The dictionary contains 127069 entries.  Of these, 119400 words are assigned
# a unique pronunciation, 6830 words have two pronunciations, and 839 words have
# three or more pronunciations.  Many of these are fast-speech variants.
# https://www.nltk.org/_modules/nltk/corpus/reader/cmudict.html
arpabet = nltk.corpus.cmudict.dict()

# Change this to the port your Arduino is connected to.
serial_port = serial.Serial("COM3", 9600)


def text_to_speech(user_input):
    # Set the text input to be synthesized.
    synthesis_input = texttospeech.SynthesisInput(text=user_input)

    # Build the voice request, select language code ("en-US") and the ssml voice gender ("female").
    voice = texttospeech.VoiceSelectionParams(language_code="en-US",
                                              name="en-US-Wavenet-F",
                                              ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)

    # Selects the type of audio file to return.
    audio_config = texttospeech.AudioConfig(speaking_rate=1.0,
                                            audio_encoding=texttospeech.AudioEncoding.MP3)

    # Instantiates a client.
    client = texttospeech.TextToSpeechClient()

    # Initializes mixer.
    mixer.init()

    # Performs the text-to-speech request on the text input with the selected voice parameters and audio file type.
    synthetic_response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    # Writes the synthetic audio to the output file.
    with open("synthetic.mp3", "wb") as out:
        out.write(synthetic_response.audio_content)

    # Plays the synthetic audio.
    mixer.music.load("synthetic.mp3")
    mixer.music.play()

    # Waits for audio to finish playing and stops the audio.
    while mixer.music.get_busy():
        time.sleep(1)
    mixer.music.stop()

    # Unloads the synthetic audio from resource allocation.
    mixer.music.unload()

    # Deletes the created audio files.
    os.remove("synthetic.mp3")


def speech_to_text():
    # Sample rate.
    fs = 44100
    # Duration of recording.
    seconds = 6
    # Speech recognizer.
    recognizer = speech_recognition.Recognizer()

    print("Recording...")
    my_recording = sounddevice.rec((seconds * fs), samplerate=fs, channels=1)
    sounddevice.wait()  # Wait until recording is finished
    write("raw_recording.wav", fs, my_recording)  # Save as WAV file
    print("Processing...")

    # Converts wav file to readable wave file.
    # Future improvement: find a way to not have to convert the wav file.
    sound = AudioSegment.from_wav("raw_recording.wav")
    sound.export("recording.wav", format="wav")

    microphone = speech_recognition.AudioFile("recording.wav")
    with microphone as source:
        audio = recognizer.record(source)

    # Deletes the created audio files.
    os.remove("raw_recording.wav")
    os.remove("recording.wav")

    # Print and return recording.
    print("You said:", recognizer.recognize_google(audio))
    return recognizer.recognize_google(audio)


def mouth_articulation(your_sentence):
    #  Separates the input sentence into a list, converts all characters to lowercase, and strips away punctuation.
    your_sentence = your_sentence.lower().translate(str.maketrans("", "", string.punctuation))
    your_sentence = your_sentence.split()
    print("You Typed:", your_sentence)

    # Finds an ARPAbet translation of each word in the sentence and stores it in the result array.
    result = []
    for words in your_sentence:
        result.append(arpabet[words])
    array_length = len(result)

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


def lem_tokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


def lem_normalize(text):
    return lem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_dict)))


def greeting(sentence):
    # If user's input is a greeting, return a greeting response.
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Generating response.
def response(response_from_user):
    dorothy_response = ""
    sent_tokens.append(response_from_user)
    tfidf_vector = TfidfVectorizer(tokenizer=lem_normalize, stop_words="english")
    tfidf = tfidf_vector.fit_transform(sent_tokens)
    values = cosine_similarity(tfidf[-1], tfidf)
    idx = values.argsort()[0][-2]
    flat = values.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if req_tfidf == 0:
        dorothy_response = dorothy_response + "I'm sorry! I don't understand you"
        return dorothy_response
    else:
        dorothy_response = dorothy_response + sent_tokens[idx]
        return dorothy_response


# Introduction.
print(intro)
mouth_articulation(intro)
text_to_speech(intro)
flag = True

# Main loop.
while flag is True:
    try:
        user_response = speech_to_text()
        user_response = user_response.lower()
        if "bye" in user_response:
            flag = False
            text_to_speech("Bye! Take care.")
            mouth_articulation("Bye! Take care.")

        else:
            if "thanks" in user_response or "thank you" in user_response:
                mouth_articulation("You're welcome.")
                text_to_speech("You're welcome.")
                continue

            if "search" in user_response:
                print("Dorothy:", wikipedia.summary(user_response, sentences=2))
                mouth_articulation(wikipedia.summary(user_response, sentences=2))
                text_to_speech(wikipedia.summary(user_response, sentences=2))

            else:
                if greeting(user_response) is not None:
                    this_greeting = greeting(user_response)
                    print("Dorothy:", this_greeting)
                    mouth_articulation(this_greeting)
                    text_to_speech(this_greeting)

                else:
                    print(end="")
                    this_response = response(user_response)
                    print("Dorothy:", this_response)
                    mouth_articulation(this_response)
                    text_to_speech(this_response)
                    sent_tokens.remove(user_response)

    except speech_recognition.UnknownValueError:
        repeat_that = "I'm sorry! I didn't hear what you said. Can you please repeat that?"
        print(repeat_that)
        mouth_articulation(repeat_that)
        text_to_speech(repeat_that)
        continue

    except wikipedia.exceptions.PageError:
        no_results = "I'm sorry! I couldn't find anything about that. Could you please try a different search phrase?"
        print(no_results)
        mouth_articulation(no_results)
        text_to_speech(no_results)
        continue
