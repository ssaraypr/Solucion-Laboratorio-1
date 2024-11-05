from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

def obtener_recomendacion (dataset, Titulo):
    '''
    '''
            
    #Verificar que las columnas Title/genre_1_name/original_language sean tipo string
    dataset["title"] = dataset["title"].astype("string")
    dataset["genre_1_name"] = dataset["genre_1_name"].astype("string")
    
    # Se convierte las columnas title/genero(genre_1_name)/original_language a una representación numérica usando TF-IDF
    vectorizar = TfidfVectorizer()
    title_tf = vectorizar.fit_transform(dataset["title"])
    genero_tf = vectorizar.fit_transform(dataset["genre_1_name"])
            
    #Se añade las columnas númericas a la matriz de características
    #Se usaran las variables vote_average/vote_count/popularity/genero
    #Característias para el sistema de recomendación
    features = np.column_stack([title_tf.toarray(), genero_tf.toarray(), dataset["vote_average"], dataset["vote_count"], dataset["popularity"]])
    
    #Se reindexa el index
    dataset = dataset.reset_index(drop=True)

    # Se calcula la matriz de similitud de coseno
    similarity_matrix = cosine_similarity(features)

    #Se filtra el dataset por la película buscada
    Titulo = Titulo.lower().strip()
    pelicula = dataset[dataset["title"].str.lower() == Titulo]

    if pelicula.empty:
        return "Película No encontrada"
    
    #Buscar la película por el indice
    pelicula_index = pelicula.index[0]
    peliculas_similares = similarity_matrix[pelicula_index]
    peliculas_mas_sim = np.argsort(-peliculas_similares)

    #Se obtiene la lista de las 5 películas más similares
    top_5 = dataset.loc[peliculas_mas_sim[1:6], "title"]

    resultado = {"Las 5 películas más similares a": Titulo, "son": top_5.reset_index().to_dict(orient="records")}
    return resultado

@app.get("/recomendacion/{titulo}", response_model= dict)

async def recomendacion (Titulo: str):
    '''
    '''
    try:
        movies = pd.read_csv(r"C:\Users\SARAY\Documents\Cursos Cortos\Henry\Laboratorios Individual\Laboratorio 1\Solucion Laboratorio 1\Datasets\movies_recomendación.csv")


        #Aplicar función
        resultado = obtener_recomendacion(movies, Titulo)
        return JSONResponse(content=jsonable_encoder(resultado), media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")
    