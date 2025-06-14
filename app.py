import streamlit as st
import pandas as pd
from recomendacao import recomendar_filmes

# Carregamento adicional
links = pd.read_csv('links.csv')
filmes = pd.read_csv('movies.csv')
lista_titulos = filmes['title'].values.tolist()

# Função para pegar o pôster com IMDB
def get_poster(imdb_id):
    url = f"https://img.omdbapi.com/?i=tt{str(imdb_id).zfill(7)}&apikey=c2a06ac8"
    return url

# Interface
st.title("🎬 Recomendador de Filmes")

filme_usuario = st.selectbox("Digite o nome de um filme que você gosta:", lista_titulos)

if st.button("Mostrar Recomendações"):
    recomendados = recomendar_filmes(filme_usuario)

    if recomendados:
        st.subheader("Filmes recomendados:")
        for titulo in recomendados:
            movie_id = filmes[filmes['title'] == titulo]['movieId'].values[0]
            imdb_id = links[links['movieId'] == movie_id]['imdbId'].values[0]
            poster_url = get_poster(imdb_id)

            st.markdown(f"### {titulo}")
            st.image(poster_url, width=150)
            st.markdown(f"**IMDB ID:** tt{str(imdb_id).zfill(7)}")
    else:
        st.warning("Filme não encontrado ou sem recomendações disponíveis.")
