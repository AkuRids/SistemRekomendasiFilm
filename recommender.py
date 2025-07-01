import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("netflix_titles.csv")
df = df[df['type'] == 'Movie'].copy()
df.fillna('', inplace=True)

# Gabungkan konten
df['combined_features'] = df['title'] + ' ' + df['director'] + ' ' + df['cast'] + ' ' + df['listed_in'] + ' ' + df['description']

# TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])

# Cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Reset index
df = df.reset_index()

# Bikin daftar judul dalam lowercase
df['title_lower'] = df['title'].str.lower().str.strip()

# Fungsi rekomendasi dengan toleransi kesalahan input
def recommend(title, top_n=5):
    title = title.lower().strip()
    if title not in df['title_lower'].values:
        similar_titles = df[df['title_lower'].str.contains(title[:3])]['title'].unique().tolist()
        suggestions = "\n- ".join(similar_titles[:5])
        return f"Judul '{title}' tidak ditemukan. Coba salah satu dari:\n- {suggestions if suggestions else 'Tidak ada saran judul mirip'}"

    idx = df[df['title_lower'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]

    return df[['title', 'description', 'type', 'country', 'release_year']].iloc[movie_indices]
