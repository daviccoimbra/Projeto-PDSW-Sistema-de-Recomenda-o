import numpy as np
import pandas as pd
import difflib
#from sklearn.metrics.pairwise import cosine_similarity

filmes = pd.read_csv('movies.csv')
notas = pd.read_csv('ratings.csv')
links = pd.read_csv('links.csv')

coluna_filmes = filmes[['movieId','title']]
coluna_notas = notas[['userId','movieId','rating']]
filmes_data = pd.merge(coluna_filmes, coluna_notas)
filmes_pivot = filmes_data.pivot_table(index=['userId'], columns=['title'], values='rating')

def recomendar_filmes(filme_input, minimo_avaliacoes=500, top_n=10):
    lista_titulos = coluna_filmes['title'].tolist()
    encontrar_filme = difflib.get_close_matches(filme_input, lista_titulos, n=1)

    if not encontrar_filme:
        return []

    filme = encontrar_filme[0]
    filme_rating = filmes_pivot[filme]
    similaridade = filmes_pivot.corrwith(filme_rating)

    corr_filmes = pd.DataFrame(similaridade, columns=['correlacao'])
    corr_filmes.dropna(inplace=True)

    quantidade_avaliacoes = filmes_data.groupby('title')['rating'].count()
    corr_filmes = corr_filmes.join(quantidade_avaliacoes)
    recomendacoes = corr_filmes[corr_filmes['rating'] > minimo_avaliacoes]\
                        .sort_values('correlacao', ascending=False)

    resultado = recomendacoes.head(top_n).index.tolist()
    return resultado