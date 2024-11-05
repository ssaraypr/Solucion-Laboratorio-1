from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

@app.get("/recomendacion/{titulo}")

def recomendacion (Titulo: str):
    '''
    '''
    #Acceder al archivo de Movies
    movies = pd.read_csv("Datasets/movies_recomendación.csv")
          
    #Verificar que las columnas Title/genre_1_name/original_language sean tipo string
    movies["title"] = movies["title"].astype("string")
    movies["genre_1_name"] = movies["genre_1_name"].astype("string")
    
    # Se convierte las columnas title/genero(genre_1_name)/original_language a una representación numérica usando TF-IDF
    vectorizar = TfidfVectorizer()
    title_tf = vectorizar.fit_transform(movies["title"])
    genero_tf = vectorizar.fit_transform(movies["genre_1_name"])
            
    #Se añade las columnas númericas a la matriz de características
    #Se usaran las variables vote_average/vote_count/popularity/genero
    #Característias para el sistema de recomendación
    features = np.column_stack([title_tf.toarray(), genero_tf.toarray(), movies["vote_average"], movies["vote_count"], movies["popularity"]])
    
    #Se reindexa el index
    movies = movies.reset_index(drop=True)

    # Se calcula la matriz de similitud de coseno
    similarity_matrix = cosine_similarity(features)

    #Se filtra el dataset por la película buscada
    Titulo = Titulo.lower().strip()
    pelicula = movies[movies["title"].str.lower() == Titulo]

    if not pelicula.empty:
        pelicula_index = pelicula.index[0]
        peliculas_similares = similarity_matrix[pelicula_index]
        peliculas_mas_sim = np.argsort(-peliculas_similares)

        #Se obtiene la lista de las 5 películas más similares
        top_5 = movies.loc[peliculas_mas_sim[1:6], "title"]

        resultado = {"Las 5 películas más similares a": Titulo, "son": top_5.reset_index().to_dict(orient="records")}
        return JSONResponse(content=jsonable_encoder(resultado), media_type="application/json")
    else:
        return "Película No encontrada"