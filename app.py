
# import streamlit as st
# from get_review import recommend, recommend_by_genre, discover_indian_movies

# if "recs" not in st.session_state:
#     st.session_state.recs = None
# st.set_page_config(page_title="Smart Stream", layout="wide")

# # ✅ SESSION STATE
# if "selected_movie" not in st.session_state:
#     st.session_state.selected_movie = None

# st.title("🎬 Smart Stream AI")

# st.markdown("""
# <style>
# @media (max-width: 768px) {
#     img {
#         width: 100% !important;
#     }
# }
# </style>
# """, unsafe_allow_html=True)

# # 🎨 HOVER EFFECT
# st.markdown("""
# <style>
# img {
#     transition: transform 0.3s ease;
# }
# img:hover {
#     transform: scale(1.05);
#     cursor: pointer;
# }
# </style>
# """, unsafe_allow_html=True)

# st.markdown("### Movie Recommendation System 🍿")

# # 🎬 DETAILS PAGE
# def show_movie_details(movie):

#     if st.button("⬅ Back"):
#         st.session_state.selected_movie = None
#         st.rerun()

#     st.title(movie.get("title", "No Title"))

#     col1, col2 = st.columns([1, 2])

#     # 🎬 LEFT
#     with col1:
#         if movie.get("poster"):
#             st.image(movie["poster"], use_container_width=True)

#         st.markdown(f"⭐ {movie.get('rating','N/A')} / 10")

#         if movie.get("release_date"):
#             st.markdown(f"📅 {movie['release_date']}")

#         if movie.get("runtime"):
#             st.markdown(f"⏱ {movie['runtime']} min")

#         if movie.get("genres"):
#             st.markdown("🎭 " + ", ".join(movie["genres"]))

#     # 🎬 RIGHT
#     with col2:
#         st.subheader("Overview")
#         st.write(movie.get("overview", "No description available"))

#         if movie.get("trailer"):
#             st.subheader("▶ Trailer")
#             st.video(movie["trailer"])

#     # 🎭 CAST (Responsive Grid)
#     if movie.get("cast"):
#         st.subheader("🎭 Top Cast")

#         cols = st.columns(5)

#         for idx, actor in enumerate(movie["cast"][:5]):
#             with cols[idx]:
#                 if actor.get("photo"):
#                     st.image(actor["photo"], use_container_width=True)
#                 st.caption(actor.get("name"))

#     # 💬 REVIEWS (Better UI)
#     if movie.get("reviews"):
#         st.subheader("💬 Reviews")

#         for r in movie["reviews"]:
#             st.markdown(f"""
#             <div style='background:#1e1e1e;padding:10px;border-radius:10px;margin-bottom:10px'>
#                 <b>{r.get('author','User')}</b><br>
#                 {r.get('content','')}
#             </div>
#             """, unsafe_allow_html=True)

#     # 🔥 SIMILAR MOVIES

#     # 🔥 SIMILAR MOVIES
#     if movie.get("id"):
#         from get_review import fetch_similar_movies

#     similar = fetch_similar_movies(movie["id"])
#     cols = st.columns(6)

#     for idx, sm in enumerate(similar):
#         with cols[idx]:

#         # 🎬 POSTER
#             if sm.get("poster"):
#                 st.image(sm["poster"], use_container_width=True)
#                 st.caption(sm.get("title"))
#                 st.markdown(f"⭐ {sm.get('rating','N/A')}")

#         # 🎬 VIEW BUTTON (🔥 NEW)
#             if st.button("🎬 View", key=f"sim_view_{idx}", use_container_width=True):
            
#             # 🔥 IMPORTANT: fetch full details
#                 from get_review import fetch_movie_details, fetch_movie_trailer, fetch_movie_cast, fetch_movie_reviews

#                 details = fetch_movie_details(sm["title"])

#                 if details:
#                     details["trailer"] = fetch_movie_trailer(sm["title"])
#                     details["cast"] = fetch_movie_cast(sm["title"])
#                     details["reviews"] = fetch_movie_reviews(sm["title"])

#                 st.session_state.selected_movie = details
#                 st.rerun()

#         # 🎬 INFO

#         # if similar:
#         #     st.subheader("🎯 Similar Movies")

#         #     cols = st.columns(6)

#         #     for idx, sm in enumerate(similar):
#         #         with cols[idx]:
#         #             if sm.get("poster"):
#         #                 st.image(sm["poster"], use_container_width=True)
#         #             st.caption(sm.get("title"))
#         #             st.markdown(f"⭐ {sm.get('rating','N/A')}")
#     # 💬 REVIEWS
#     if movie.get("reviews"):
#         st.subheader("💬 Reviews")
#         for r in movie["reviews"]:
#             st.write(f"**{r.get('author','User')}**: {r.get('content','')}")


# # ✅ PAGE SWITCH
# if st.session_state.selected_movie:
#     show_movie_details(st.session_state.selected_movie)
#     st.stop()


# # 🎯 OPTIONS
# option = st.selectbox(
#     "🎯 Choose Recommendation Type",
#     ["Search by Movie Name", "Discover by Genre", "Trending in India 🇮🇳"]
# )

# recs = None

# # 🔍 SEARCH
# if option == "Search by Movie Name":
#     movie_name = st.text_input("🔍 Enter Movie Name")

#     if st.button("✨ Recommend"):
#         if movie_name.strip():
#             with st.spinner("🔎 Finding movies..."):
#                 st.session_state.recs = recommend(movie_name)
#         else:
#             st.warning("⚠️ Enter a movie name")


# # 🎭 GENRE
# elif option == "Discover by Genre":
#     genre = st.selectbox(
#         "🎭 Select Genre",
#         ["Action", "Comedy", "Romance", "Thriller", "Horror", "Adventure", "Animation"]
#     )

#     if st.button("🎯 Find Movies"):
#         with st.spinner("🎬 Loading movies..."):
#             st.session_state.recs = recommend_by_genre(genre)


# # 🇮🇳 TRENDING
# elif option == "Trending in India 🇮🇳":
#     if st.button("🔥 Show Trending"):
#         with st.spinner("📈 Fetching trending movies..."):
#             st.session_state.recs = discover_indian_movies()


# # 🎬 DISPLAY SECTION
# recs = st.session_state.recs

# if recs:

#     # ❌ HANDLE ERROR STRING
#     if isinstance(recs, str):
#         st.error(recs)

#     # ✅ HANDLE LIST
#     elif isinstance(recs, list) and len(recs) > 0:

#         st.markdown("## 🔥 Movies For You")

#         cols = st.columns(5)

#         for idx, movie in enumerate(recs):

#             if not isinstance(movie, dict):
#                 continue

#             with cols[idx % 5]:

#                 # POSTER
#                 if movie.get("poster"):
#                     st.image(movie["poster"], use_container_width=True)

#                 # BUTTON
#                 if st.button(f"🎬 View", key=f"view_{idx}", use_container_width=True):
#                     st.session_state.selected_movie = movie
#                     st.session_state.recs = recs  # preserve
#                     st.rerun()

#                 # INFO
#                 st.markdown(f"**{movie.get('title','No Title')}**")
#                 st.markdown(f"⭐ {movie.get('rating','N/A')} / 10")

#                 overview = movie.get('overview') or ""
#                 st.caption(overview[:100] + "..." if overview else "No description")

#     else:
#         st.warning("⚠️ No movies found")

#         if st.button("Recommend"):
#             with st.spinner("Finding best movies for you... 🎬"):
#                 recs = recommend(movie_name)

#         if not recs or (isinstance(recs, list) and "error" in recs[0]):
#             st.warning("⚠️ Movie not found. Try another name.")
#         else:
#             st.session_state.recs = recs


import streamlit as st
from get_review import (
    recommend,
    recommend_by_genre,
    discover_indian_movies,
    get_trending_movies,
    fetch_similar_movies,
    fetch_movie_details,
    fetch_movie_trailer,
    fetch_movie_cast,
    fetch_movie_reviews,
    GENRE_MAP
)

st.set_page_config(page_title="Smart Stream", layout="wide")

# =========================
# SESSION STATE
# =========================
if "recs" not in st.session_state:
    st.session_state.recs = None

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None

st.title("🎬 Smart Stream AI")
st.markdown("### Movie Recommendation System 🍿")

# =========================
# DETAILS PAGE
# =========================
def show_movie_details(movie):

    if not movie:
        st.error("❌ Movie data not found")
        return

    if st.button("⬅ Back"):
        st.session_state.selected_movie = None
        st.rerun()

    st.title(movie.get("title", "No Title"))

    col1, col2 = st.columns([1, 2])

    # LEFT
    with col1:
        if movie.get("poster"):
            st.image(movie["poster"], use_container_width=True)

        st.markdown(f"⭐ {movie.get('rating','N/A')} / 10")
        st.markdown(f"📅 {movie.get('release_date','N/A')}")
        st.markdown(f"⏱ {movie.get('runtime','N/A')} min")

        if movie.get("genres"):
            st.markdown("🎭 " + ", ".join(movie["genres"]))

    # RIGHT
    with col2:
        st.subheader("Overview")
        st.write(movie.get("overview", "No description"))

        if movie.get("trailer"):
            st.subheader("▶ Trailer")
            st.video(movie["trailer"])

    # =========================
    # CAST
    # =========================
    if movie.get("cast"):
        st.subheader("🎭 Top Cast")

    cast = movie.get("cast", [])

    for i in range(0, len(cast), 6):   # 👈 rows of 6
        cols = st.columns(6)

        for j in range(6):
            if i + j < len(cast):
                actor = cast[i + j]

                with cols[j]:
                    if actor.get("photo"):
                        st.image(actor["photo"], use_container_width=True)
                        st.caption(actor.get("name"))

    # =========================
    # REVIEWS
    # =========================
    if movie.get("reviews"):
        st.subheader("💬 Reviews")

        for r in movie["reviews"]:
            st.markdown(f"""
            <div style='background:#1e1e1e;padding:10px;border-radius:10px;margin-bottom:10px'>
                <b>{r.get('author','User')}</b><br>
                {r.get('content','')}
            </div>
            """, unsafe_allow_html=True)

    # =========================
    # SIMILAR MOVIES (🔥 FIXED)
    # =========================
    if movie.get("id"):

        similar = fetch_similar_movies(movie["id"])

        if similar:
            st.subheader("🎯 Similar Movies")

            cols = st.columns(min(len(similar), 6))

            for idx, sm in enumerate(similar):

                if not sm:
                    continue

                with cols[idx % len(cols)]:

                    if sm.get("poster"):
                        st.image(sm["poster"], use_container_width=True)

                    st.caption(sm.get("title"))
                    st.markdown(f"⭐ {sm.get('rating','N/A')}")

                    if st.button("🎬 View", key=f"sim_{idx}", use_container_width=True):

                        details = fetch_movie_details(sm.get("title"))

                        if not details:
                            st.warning("Details not found")
                            continue

                        details["id"] = sm.get("id")
                        details["trailer"] = fetch_movie_trailer(sm.get("title"))
                        details["cast"] = fetch_movie_cast(sm.get("title"), limit=10)
                        details["reviews"] = fetch_movie_reviews(sm.get("title"))

                        st.session_state.selected_movie = details
                        st.rerun()

# =========================
# PAGE SWITCH
# =========================
if st.session_state.selected_movie:
    show_movie_details(st.session_state.selected_movie)
    st.stop()

# =========================
# OPTIONS
# =========================
option = st.selectbox(
    "🎯 Choose Recommendation Type",
    ["Search by Movie Name", "Discover by Genre", "Trending in India 🇮🇳"]
)

# =========================
# SEARCH
# =========================
if option == "Search by Movie Name":
    movie_name = st.text_input("🔍 Enter Movie Name")

    if st.button("✨ Recommend"):
        if movie_name.strip():
            with st.spinner("🔎 Finding movies..."):
                st.session_state.recs = recommend(movie_name)
        else:
            st.warning("⚠️ Enter a movie name")

# =========================
# GENRE
# =========================
elif option == "Discover by Genre":
    selected_genre = st.selectbox(
    "Select Genre",
    list(GENRE_MAP.keys())
)
    if st.button("🎯 Find Movies"):
        with st.spinner("🎬 Loading..."):
            genre_movies = recommend_by_genre(selected_genre)

# =========================
# TRENDING
# =========================
elif option == "Trending in India 🇮🇳":

    if st.button("🎯 Find Movies"):
        with st.spinner("📈 Fetching..."):
            st.session_state.recs = discover_indian_movies()

    if st.session_state.recs:
        st.subheader("🇮🇳 Trending in India")

elif option == "Global Trending":
    st.subheader("🌍 Global Trending")
    with st.spinner("📈 Fetching..."):
        st.session_state.recs = get_trending_movies()
    

# =========================
# DISPLAY RESULTS
# =========================
recs = st.session_state.recs

if recs:

    if isinstance(recs, str):
        st.error(recs)

    elif isinstance(recs, list) and len(recs) > 0:

        st.markdown("## 🔥 Movies For You")

        cols = st.columns(5)

        for idx, movie in enumerate(recs):

            if not movie:
                continue

            with cols[idx % 5]:

                if movie.get("poster"):
                    st.image(movie["poster"], use_container_width=True)

                if st.button("🎬 View", key=f"main_{idx}", use_container_width=True):
                    st.session_state.selected_movie = movie
                    st.rerun()

                st.markdown(f"**{movie.get('title','No Title')}**")
                st.markdown(f"⭐ {movie.get('rating','N/A')}")

                overview = movie.get("overview") or ""
                st.caption(overview[:100] + "..." if overview else "No description")

    else:
        st.warning("⚠️ No movies found")