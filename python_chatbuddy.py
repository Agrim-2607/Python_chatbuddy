import nltk
import string
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# download once
nltk.download('punkt')
nltk.download('wordnet')

# Load training data
with open("python.txt", "r", encoding="utf-8") as file:
    data = file.read()

sent_tokens = nltk.sent_tokenize(data)
 
# Preprocessing
lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct = dict((ord(p), None) for p in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct)))


# def greet(sentence):
    

# TF-IDF vectorizer
vectorizer = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
tfidf = vectorizer.fit_transform(sent_tokens)

# responses={}
# Chatbot response function
Greet_inputs=("hello","hi","hey","what's up","sup","greetings")
Greet_responses=("hi","hey","*nods*","hi there","hello","I'm glad! you are talking to me")
def chatbot_response(user_input):

    for word in user_input.split():
        if word.lower() in Greet_inputs:
            return random.choice(Greet_responses)

    user_input = user_input.lower()
    user_vector = vectorizer.transform([user_input])

    similarity = cosine_similarity(user_vector, tfidf)
    index = similarity.argsort()[0][-1]

    score = similarity[0][index]

    if score < 0.1:
        return "I don't know the answer. Add more training data."

    else:
        return sent_tokens[index]

# Chat loop
print("Namaste! i m your python assisstent chatbuddy")  
print("Python Chatbot ready. Type 'exit' to stop.")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    else:
        # print("chatbot: ", greet(user_input))
        print("Chatbot:", chatbot_response(user_input),)