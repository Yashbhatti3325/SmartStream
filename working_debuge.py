import pandas as pd
import requests
import re
from sklearn.metrics.pairwise import cosine_similarity

# LOAD DATA
movies = pd.read_csv("ml-latest-small/movies.csv")
ratings = pd.read_csv("ml-latest-small/ratings.csv")

print("Movies Data Loaded:")
print(movies.head())

# CLEAN TITLE FUNCTION
def clean_title(title):
    title = re.sub(r"\(\d{4}\)", "", title)   # remove year
    title = re.sub(r"\(.*?\)", "", title)     # remove extra text
    return title.strip()

# CREATE PIVOT TABLE
movie_pivot = ratings.pivot_table(index='movieId', columns='userId', values='rating')
movie_pivot.fillna(0, inplace=True)

# SIMILARITY MATRIX
similarity = cosine_similarity(movie_pivot)

# TMDB API
API_KEY = "f9ee00e02832359dbb7c5ed8b9d32d8d"
def fetch_movie_details(title):
    for _ in range(2):  # retry 2 times
        try:
            url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
            
            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "application/json"
                }
            )

            data = response.json()

            if 'results' in data and len(data['results']) > 0:
                movie = data['results'][0]

                return {
                    "title": movie.get('title'),
                    "overview": movie.get('overview'),
                    "rating": movie.get('vote_average'),
                    "poster": "https://image.tmdb.org/t/p/w500" + movie['poster_path']
                              if movie.get('poster_path') else None
                }

        except:
            continue

    return None

# RECOMMEND FUNCTION
def recommend(movie_name):
    
    movie_match = movies[movies['title'].str.contains(movie_name, case=False)]

    if movie_match.empty:
        return "❌ Movie not found"
    
    movie_id = movie_match.iloc[0]['movieId']

    if movie_id not in movie_pivot.index:
        return "❌ Movie not in rating data"

    idx = list(movie_pivot.index).index(movie_id)

    distances = similarity[idx]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    results = []

    for i in movie_list:
        similar_movie_id = movie_pivot.index[i[0]]

        title = movies[movies['movieId'] == similar_movie_id]['title'].values[0]

        # 🔥 CLEAN TITLE HERE
        cleaned_title = clean_title(title)

        details = fetch_movie_details(cleaned_title)

        if details:
            results.append(details)

    return results

# TEST
recs = recommend("Toy Story")

print("\n🎬 Recommended Movies:\n")

if isinstance(recs, list):
    for movie in recs:
        print("Title:", movie['title'])
        print("Rating:", movie['rating'])
        print("Overview:", movie['overview'])
        print("Poster:", movie['poster'])
        print("-" * 50)
else:
    print(recs)
