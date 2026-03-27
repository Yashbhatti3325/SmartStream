
# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# For emoji support in print statements
import sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv("IMDB Dataset.csv")

df['Sentiment'] = df['sentiment'].map({'positive': 1, 'negative': 0})

X = df['review']
y = df['Sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

vectorizer = TfidfVectorizer(stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression()
model.fit(X_train_vec, y_train)

user_input = input("Enter your movie review: ")
user_input_vec = vectorizer.transform([user_input])

prediction = model.predict(user_input_vec)

import random

positive_emojis = ["😊", "😁", "😍", "😄", "🥳"]
negative_emojis = ["😡", "😢", "😞", "😠", "😭"]

if prediction[0] == 1:
    emoji = random.choice(positive_emojis)
    print("Positive", random.choice(positive_emojis))
else:
    emoji = random.choice(negative_emojis)
    print("Negative", random.choice(negative_emojis))

