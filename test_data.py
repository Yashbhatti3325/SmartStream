import pandas as pd

# Load datasets from your folder
movies = pd.read_csv("ml-latest-small/movies.csv")
ratings = pd.read_csv("ml-latest-small/ratings.csv")

# Show first 5 rows
print("Movies Data:\n", movies.head())
print("\nRatings Data:\n", ratings.head())

# # Extra (for understanding)
# print("\nMovies Shape:", movies.shape)
# print("Ratings Shape:", ratings.shape)