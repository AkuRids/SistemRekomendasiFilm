import streamlit as st
from recommender import recommend

st.title("🎬 Sistem Rekomendasi Film Netflix")
st.write("Rekomendasi berdasarkan kesamaan konten (Content-Based Filtering)")

movie_input = st.text_input("Masukkan judul film Netflix:")

if movie_input:
    recommendations = recommend(movie_input)
    
    if isinstance(recommendations, str):
        st.warning(recommendations)
    else:
        st.subheader("Hasil Rekomendasi:")
        for _, row in recommendations.iterrows():
            st.markdown(f"""
            ### 🎥 {row['title']}
            - **Tipe**: {row['type']}
            - **Negara**: {row['country'] if row['country'] else 'Tidak diketahui'}
            - **Tahun Rilis**: {row['release_year']}
            - **Deskripsi**: {row['description']}
            """)
