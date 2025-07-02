# app.py

import streamlit as st
from recommender import recommend

st.title("🎬 Sistem Rekomendasi Netflix")
st.write("Rekomendasi berdasarkan kesamaan konten (Content-Based Filtering)")

# Opsi jenis konten
filter_option = st.selectbox(
    "Tampilkan rekomendasi untuk:",
    ["Semua", "Movie", "TV Show"]
)

# Input judul
movie_input = st.text_input("Masukkan judul film atau acara Netflix:")

# Jika ada input
if movie_input:
    recommendations = recommend(movie_input)

    if isinstance(recommendations, str):
        st.warning(recommendations)
    else:
        # Filter sesuai pilihan
        if filter_option != "Semua":
            recommendations = recommendations[recommendations['type'] == filter_option]

        if recommendations.empty:
            st.info(f"Tidak ada rekomendasi bertipe {filter_option} untuk judul tersebut.")
        else:
            st.subheader("Hasil Rekomendasi:")
            for _, row in recommendations.iterrows():
                st.markdown(f"""
                ### 🎞️ {row['title']}
                - **Tipe**: {row['type']}
                - **Negara**: {row['country'] if row['country'] else 'Tidak diketahui'}
                - **Tahun Rilis**: {row['release_year']}
                - **Deskripsi**: {row['description']}
                """)
