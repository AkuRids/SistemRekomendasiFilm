# recommender.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("netflix_titles.csv")

# Hanya ambil film saja
df = df[df['type'] == 'Movie'].copy()

# Isi NaN dengan string kosong
df.fillna('', inplace=True)

# Gabungkan kolom yang relevan untuk konten
df['combined_features'] = df['title'] + ' ' + df['director'] + ' ' + df['cast'] + ' ' + df['listed_in'] + ' ' + df['description']

# TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])

# Similartiy matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Reset index agar sesuai
df = df.reset_index()

# Fungsi rekomendasi
def recommend(title, top_n=5):
    idx = df[df['title'].str.lower() == title.lower()].index
    if len(idx) == 0:
        return f"Tidak ditemukan judul '{title}' di data."
    idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]
    return df[['title', 'description']].iloc[movie_indices]
