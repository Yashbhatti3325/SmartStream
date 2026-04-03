# 🎬 SmartStream – Movie Recommendation System

SmartStream is an intelligent movie recommendation system that helps users discover movies based on their preferences using **Collaborative Filtering** and **TMDB API integration**.

It provides personalized suggestions, trending movies, genre-based discovery, and detailed movie insights — all in a clean and interactive UI built with **Streamlit**.

---

## 🚀 Features

* 🔍 **Search Movies** – Find any movie instantly
* 🎯 **Personalized Recommendations** – Based on similarity algorithms
* 📊 **Collaborative Filtering** – Uses user rating patterns
* 🎭 **Genre-Based Suggestions** – Explore movies by category
* 🇮🇳 **Indian Movies Section** – Discover Indian cinema
* 🔥 **Trending Movies** – Real-time trending movies from TMDB
* 🎬 **Movie Details View** – Ratings, overview, cast & posters
* 🎞️ **Similar Movies Section** – Explore related movies easily

---

## 🧠 Recommendation Logic

SmartStream uses:

* **Cosine Similarity** to find similar movies
* **User-Movie Rating Matrix** from dataset
* Hybrid approach:

  * Dataset-based recommendations
  * API-based discovery (TMDB)

---

## 🛠️ Tech Stack

* **Frontend/UI:** Streamlit
* **Backend:** Python
* **Libraries:**

  * Pandas
  * Scikit-learn
  * Requests
* **API:** TMDB (The Movie Database API)
* **Dataset:** MovieLens (ml-latest-small)

---

## 📂 Project Structure

```
SmartStream/
│
├── app.py                # Main Streamlit application
├── get_review.py        # Recommendation & API logic
├── movies.csv
├──ratings.csv
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/SmartStream.git
cd SmartStream
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Add TMDB API Key

* Go to https://www.themoviedb.org/
* Create an account and get your API key
* Add it inside `get_review.py`:

```python
API_KEY = "your_api_key_here"
```

### 4️⃣ Run the App

```bash
streamlit run app.py
```

---

## 📊 Dashboard Modules

* 🔎 Movie Search
* 🎯 Recommendation Engine
* 🎭 Genre-Based Movies
* 🇮🇳 Indian Movies Discovery
* 🔥 Trending Movies
* 🎬 Movie Details Viewer

---

## 📸 Screenshots

* Home Page
<img width="1899" height="767" alt="image" src="https://github.com/user-attachments/assets/fe8ac332-5dd2-4ff2-b657-7c56b22bd025" />

* Search Results
<img width="1864" height="846" alt="image" src="https://github.com/user-attachments/assets/9c70e84b-d92e-4ff5-b549-bdf0a37fc628" />

* Movie Details Page
<img width="1879" height="830" alt="image" src="https://github.com/user-attachments/assets/c112103c-14c4-4874-ad40-77824d9df365" />

* Recommendation Section
<img width="1180" height="622" alt="image" src="https://github.com/user-attachments/assets/961b4659-ffe7-40f2-bb64-2a222bcef973" />




---

## 💡 Future Improvements

* ✅ User login & personalization
* ⭐ Save watchlist / favorites
* 📱 Mobile responsive UI
* 🧠 Deep Learning-based recommendations
* 🎥 Trailer integration

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork the repo and submit a pull request.

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 👨‍💻 Author

**Yash Bhatti**

* 🎓 Computer Engineering Student
* 🔐 Aspiring Cybersecurity Engineer
* 🎸 Guitar Enthusiast

---

## 🌟 Show Your Support

If you like this project, give it a ⭐ on GitHub!

---
