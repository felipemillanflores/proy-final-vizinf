import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")

alt.data_transformers.disable_max_rows()
st.title("¿Que ver en Netflix? :tv: ")

st.write(
    """Esta aplicacion busca ayudar a encontrar contenido (series/peliculas) en NETFLIX
    para usuarios que no sepan que ver, basandose en sus prioridades de tipo y de genero de contenido
    y usando notas de dos sitios especializados en puntuar peliculas y series: IMDB (International Movie Database) y TMDB (The Movie Database) sugiere las "mejores".
    Los datos usados provienen de https://www.kaggle.com/datasets/victorsoeiro/netflix-tv-shows-and-movies/code
    """
)

titulos = pd.read_csv('titles.csv')
creditos = pd.read_csv('credits.csv')

titulos['main_genre'] = titulos['genres'].apply(lambda x: None if x=='[]' else x.replace('[', '').replace(']', '').replace("'", "").split(", ")[0])
titulos = titulos.dropna(subset=['main_genre'])

space(1)
st.title("Cantidad de titulos por Genero")
space(1)
st.write(
    """ Primero veamos que generos tiene netflix para ofrecer ...
    """
)
space(1)

# input_dropdown = alt.binding_select(options=['SHOW','MOVIE'], name='type')
# selection = alt.selection_single(fields=['type'], bind=input_dropdown)

all_types = titulos.type.unique()
type_select = st.multiselect("Primero elige que prefieres... ¿Show (Series) o Movies (Peliculas=?", all_types, all_types[:2])

datos_p1 = titulos[titulos.type.isin(type_select)]

c = alt.Chart(datos_p1).mark_bar().encode(
    alt.Y('main_genre:N', sort='-x', title='Genero'),
    alt.X('count():Q', title=None),
    tooltip=['count():Q'])

st.altair_chart(c, use_container_width=True)

space(1)
st.title("Top 50 Recomendaciones")
space(1)

st.write(
    """ Ya estamos casi listos!, ahora que sabes que tiene netflix ofrecer elige uno o mas generos y te ofreceremos
    un top 50 en base a recomendaciones de criticos y usuarios. Prueba pasando el mouse por encima de cada punto
    y veras el detalle del titulo.
    Nota: Mientras mas arriba a la derecha, mejor sera la recomendacion.
    """
)

space(1)

all_genres = datos_p1.main_genre.unique()
genre_select = st.multiselect("Elige uno o mas generos para obtener recomendaciones!", all_genres, all_genres[:1])

datos_p2 = datos_p1[datos_p1.main_genre.isin(genre_select)].sort_values(by=['imdb_score','tmdb_score'], ascending=False)

d = alt.Chart(datos_p2.head(50)).mark_circle(size=60).encode(
     x='imdb_score',
     y='tmdb_score',
     color='main_genre',
     tooltip=['title', 'release_year','description'], #'title:N',
     ).interactive()

st.altair_chart(d, use_container_width=True)