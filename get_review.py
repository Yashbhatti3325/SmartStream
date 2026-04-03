import pandas as pd
import requests
import re
import time
import difflib
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# =========================
# CACHE REQUEST
# =========================
@st.cache_data(show_spinner=False)
def cached_request(url):
    return safe_request(url)

# =========================
# LOAD DATA
# =========================
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

movie_pivot = ratings.pivot_table(index='movieId', columns='userId', values='rating').fillna(0)
similarity = cosine_similarity(movie_pivot)

API_KEY = "f9ee00e02832359dbb7c5ed8b9d32d8d"  # REPLACE WITH YOUR TMDB API KEY

# =========================
# SAFE REQUEST
# =========================
def safe_request(url):
    for _ in range(3):
        try:
            r = requests.get(url)
            r.raise_for_status()
            return r.json()
        except:
            time.sleep(1)
    return None

# =========================
# CLEAN TITLE
# =========================
def clean_title(title):
    if not title:
        return ""
    title = title.lower().strip()
    title = re.sub(r'\(\d{4}\)', '', title)
    title = re.sub(r'[^a-z0-9 ]', '', title)
    return title

# =========================
# FETCH DETAILS
# =========================
def fetch_movie_details(title):
    data = cached_request(f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}")

    if not data or not data.get("results"):
        return None

    cleaned_input = clean_title(title)

    best_match = None
    best_score = 0

    for m in data["results"]:
        tmdb_title = clean_title(m.get("title", ""))
        score = difflib.SequenceMatcher(None, cleaned_input, tmdb_title).ratio()

        if score > best_score:
            best_score = score
            best_match = m

    if best_score < 0.6:
        return None

    movie_id = best_match["id"]

    details = cached_request(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}")

    if not details:
        return None

    return {
        "id": movie_id,
        "title": best_match.get("title"),
        "overview": best_match.get("overview"),
        "rating": best_match.get("vote_average"),
        "poster": "https://image.tmdb.org/t/p/w500" + best_match['poster_path']
        if best_match.get('poster_path') else None,
        "release_date": details.get("release_date"),
        "runtime": details.get("runtime"),
        "genres": [g["name"] for g in details.get("genres", [])]
    }

# =========================
# TRAILER
# =========================
def fetch_movie_trailer(title):
    data = cached_request(f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}")

    if not data or not data.get("results"):
        return None

    movie_id = data["results"][0]["id"]

    videos = cached_request(f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}")

    if not videos or not videos.get("results"):
        return None

    for v in videos["results"]:
        if v.get("type") == "Trailer" and v.get("site") == "YouTube":
            return f"https://www.youtube.com/watch?v={v['key']}"

    return None

# =========================
# CAST
# =========================
def fetch_movie_cast(title, limit=10):
    data = cached_request(f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}")

    if not data or not data.get("results"):
        return []

    movie_id = data["results"][0]["id"]

    credits = cached_request(f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}")

    if not credits or not credits.get("cast"):
        return []

    return [
        {
            "name": c.get("name"),
            "photo": "https://image.tmdb.org/t/p/w200" + c['profile_path']
            if c.get("profile_path") else None
        }
        for c in credits["cast"][:limit]
    ]

# =========================
# REVIEWS
# =========================
def fetch_movie_reviews(title):
    data = cached_request(f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}")

    if not data or not data.get("results"):
        return []

    movie_id = data["results"][0]["id"]

    reviews = cached_request(f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={API_KEY}")

    if not reviews or not reviews.get("results"):
        return [{"author": "System", "content": "No reviews available"}]

    return [
        {
            "author": r.get("author", "Unknown"),
            "content": r.get("content", "")[:200]
        }
        for r in reviews["results"][:2]
    ]

# =========================
# TMDB RECOMMEND (FIXED)
# =========================
def recommend_from_tmdb(movie_name):
    data = cached_request(f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}")

    if not data or not data.get("results"):
        return []

    results = []

    for m in data["results"][:5]:
        if not m:
            continue

        title = m.get("title")

        details = fetch_movie_details(title)

        if not details:
            continue

        details["trailer"] = fetch_movie_trailer(title)
        details["cast"] = fetch_movie_cast(title)
        details["reviews"] = fetch_movie_reviews(title)

        results.append(details)

    return results


# =========================
# GENRE RECOMMEND
# ========================

def recommend_by_genre(genre):

    if not genre:
        return []

    genre_id = GENRE_MAP.get(genre)

    if not genre_id:
        return []

    results = []

    try:
        data = cached_request(
            f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={genre_id}&sort_by=popularity.desc"
        )

        if not data or not data.get("results"):
            return []

        for m in data["results"][:5]:

            title = m.get("title")

            if not title:
                continue

            details = fetch_movie_details(title)

            if not details:
                continue

            details["id"] = m.get("id")

            details["trailer"] = fetch_movie_trailer(title)
            details["cast"] = fetch_movie_cast(title, limit=10)
            details["reviews"] = fetch_movie_reviews(title)

            results.append(details)

        return results

    except Exception as e:
        print("Genre error:", e)
        return []

# ========================
# TRENDING INDIAN
# ========================
def get_trending_movies():

    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={API_KEY}"

    data = requests.get(url).json()

    results = []

    for movie in data.get("results", [])[:10]:
        results.append({
            "title": movie.get("title"),
            "poster": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}",
            "id": movie.get("id")
        })

    return results

def discover_indian_movies():
    data = cached_request(
        f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}"
    )

    if not data or not data.get("results"):
        return []

    results = []

    for movie in data["results"]:
        if movie.get("original_language") in ['hi', 'en', 'ta', 'te', 'gu']:

            results.append({
                "id": movie.get("id"),
                "title": movie.get("title"),
                "overview": movie.get("overview"),
                "rating": movie.get("vote_average"),
                "poster": "https://image.tmdb.org/t/p/w500" + movie['poster_path']
                if movie.get('poster_path') else None
            })

        if len(results) >= 10:
            break

    return results

# ========================
# similarity recommendation
# ========================
def fetch_similar_movies(movie_id):

    if not movie_id:
        print("❌ No movie_id provided")
        return []

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={API_KEY}"
    data = cached_request(url)

    if not data:
        print("❌ API failed for similar movies")
        return []

    if not data.get("results"):
        print("⚠️ No similar movies found")
        return []

    results = []

    for m in data["results"][:6]:

        if not m:
            continue

        results.append({
            "id": m.get("id"),
            "title": m.get("title"),
            "poster": "https://image.tmdb.org/t/p/w500" + m['poster_path']
            if m.get('poster_path') else None,
            "rating": m.get("vote_average")
        })

    print("✅ Similar movies fetched:", len(results))

    return results

def find_in_dataset(movie_name, movies):
    movie_name = clean_title(movie_name)

    # ✅ Exact match first
    for i, title in enumerate(movies['title']):
        if movie_name == clean_title(title):
            return i

    # ✅ Then fallback to contains (less strict)
    for i, title in enumerate(movies['title']):
        if movie_name in clean_title(title):
            return i

    return None

def get_full_details_from_dataset(idx, movies_df, similarity):
    distances = similarity[idx]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    results = []

    for i in movie_list:
        movie = movies_df.iloc[i[0]]

        results.append({
            "title": movie.title,
            "overview": movie.overview,
            "poster": movie.poster_path,
            "rating": movie.vote_average,
            "release_date": movie.release_date
        })

    return results

def build_movie_object(details):
    if not details:
        return None

    return [{
        "title": details.get("title"),
        "overview": details.get("overview"),
        "poster": details.get("poster_path"),
        "rating": details.get("vote_average"),
        "release_date": details.get("release_date")
    }]

# =========================
# MAIN RECOMMEND
# =========================
def recommend(movie_name):
    if not movie_name:
        return []

    print("🔥 Using TMDB FIRST")

    results = recommend_from_tmdb(movie_name)

    if results:
        return results

    print("⚠️ Falling back to dataset")

    idx = None

    for i, title in enumerate(movies["title"]):
        if clean_title(movie_name) in clean_title(title):
            idx = i
            break

    if idx is None:
        return []

    distances = similarity[idx]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    final = []

    for i in movie_list:
        title = movies.iloc[i[0]].title

        d = fetch_movie_details(title)

        if not d:
            continue

        d["trailer"] = fetch_movie_trailer(title)
        d["cast"] = fetch_movie_cast(title)
        d["reviews"] = fetch_movie_reviews(title)

        final.append(d)

    return final

GENRE_MAP = {
    "Action": 28,
    "Comedy": 35,
    "Drama": 18,
    "Horror": 27,
    "Romance": 10749,
    "Thriller": 53,
    "Animation": 16,
    "Crime": 80,
    "Adventure": 12,
    "Sci-Fi": 878
}
