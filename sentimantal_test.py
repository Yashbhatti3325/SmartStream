
# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_csv("IMDB Dataset.csv")

# prepare dataset
df['sentiment'] = df['sentiment'].map({'positive': 1, 'negative': 0})

# split dataset into features and target variable
X = df['review']
y = df['sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# convert text data into numerical features using TF-IDF vectorization
vectorizer = TfidfVectorizer(stop_words='english')

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train model 
model = LogisticRegression()
model.fit(X_train_vec, y_train)

# Test accuracy
accuracy = model.score(X_test_vec, y_test)
print("Accuracy:", accuracy)


# Test your own accuracy
# sample = ["This movie is not that good. The acting was decent but the plot was predictable. I enjoyed it overall but it could have been better."]
# sample_vec = vectorizer.transform(sample)

# prediction = model.predict(sample_vec)

# if prediction[0] == 1:
#     print("Positive ")
# else:
#     print("Negative ")