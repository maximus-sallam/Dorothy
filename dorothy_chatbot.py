# Meet Dorothy: your friend.

# Import necessary libraries.
import random
import string  # to process standard python strings
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer as tfidf_vectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import nltk
from nltk.stem import WordNetLemmatizer

warnings.filterwarnings("ignore")

# For downloading packages.
nltk.download("popular",
              quiet=True)

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


# Generating response
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


flag = True
print("Dorothy: My name is Dorothy. I will answer your queries about chatbots. If you want to exit, type Bye!")
while flag:
    user_response = input()
    user_response = user_response.lower()
    if user_response != "bye":
        if user_response == "thanks" or user_response == "thank you":
            flag = False
            print("Dorothy: You are welcome..")
        else:
            if greeting(user_response) is not None:
                print("Dorothy: " + greeting(user_response))
            else:
                print("Dorothy: ",
                      end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag = False
        print("Dorothy: Bye! take care..")
