from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

@app.get("/cantidad_filmaciones_mes/{Mes}")

#Función para devolver la cantidad de películas que fueron estrenadas en el mes 
def cantidad_filmaciones_mes( Mes: str ):
    '''
    Cuenta la cantidad de peliculas estrenadas en un mes especifico
    argumentos:
    Mes: mes en formato de texto  (por ejemplo: enero, idioma español)
    Devuelve:
    El número de películas estrenadas en el mes indicado
    '''
    # Ir al archivo de movies para obtener las películas
    movies = pd.read_csv("Datasets/movies.csv")
    # Se Convierte la columna de release_date a tipo datetime
    movies["release_date"] = pd.to_datetime(movies["release_date"])
    #Incluir una columna con el nombre del mes en español
    mes_Español = {1:"enero", 2:"febrero", 3:"marzo", 4:"abril", 5:"mayo", 6:"junio", 7:"julio", 8:"agosto", 
               9:"septiembre", 10:"octubre", 11:"noviembre", 12:"diciembre"}
    movies["mes_estreno"] = movies["release_date"].dt.month.map(mes_Español)
    movies["mes_estreno"] = movies["mes_estreno"].astype("string")
    
    #Obtener la cantidad de peliculas en el mes
    movies_pormes = movies[movies["mes_estreno"] == Mes.lower()].shape[0]

    return f"{movies_pormes} cantidad de películas fueron estrenadas en el mes de {Mes}"

@app.get("/cantidad_filmaciones_dia/{Dia}")

#Función para devolver la cantidad de películas que fueron estrenadas en un día
def cantidad_filmaciones_dia (Dia : str):
    '''
    Cuenta la cantidad de películas estrenadas en un día especifico
    argumentos:
    Dia: día en españon (por ejemplo: lunes)
    Devuelve:
    El número de pelíclas estrenadas en el día indicado
    '''
    #Ir al archivo de movies para obtener las películas
    movies = pd.read_csv("Datasets/movies.csv")
    #Se convierte la columna de release_date a tipo date time
    movies["release_date"] = pd.to_datetime(movies["release_date"])
    #incluir una columna con número del día de la semana
    movies["dia_estreno"]=movies["release_date"].dt.weekday
    #Incluir una columna con el nombre del día de la semana en español
    dia_español = {0:"lunes", 1:"martes", 2:"miércoles", 3:"jueves", 4:"viernes", 5:"sábado", 6:"domingo"}
    movies["nombre_dia"] = movies["dia_estreno"].map(dia_español)
    movies["nombre_dia"] = movies["nombre_dia"].astype("string")

    #Obtener la cantidad de películas en el día
    movies_pordia = movies[movies["nombre_dia"] == Dia.lower()].shape[0]

    return f"{movies_pordia} cantidad de películas fueron estrenadas en los días {Dia}"

@app.get("/score_titulo/{Titulo}")

def score_titulo(titulo_de_la_filmación: str):
    '''
    Presenta el titulo de una película, su año de estreno y el score
    argumentos:
    titulo_de_la_filmación : Título de una filmación
    Devuelve: 
    El título de la película, el año de estreno y el score
    '''
    #Ir al archivo movies para obtener las películas
    movies = pd.read_csv("Datasets/movies.csv")

    #Colocar todo lo escrito en el titulo en minusculas para facilitar busqueda
    titulo_de_la_filmación = titulo_de_la_filmación.lower()

    #Filtrar las peliculas por el título
    pelicula = movies[movies["title"].str.lower() == titulo_de_la_filmación]

    #Si no se encuentra la película (porque busqueda fue vacía), retornar mensaje:
    if pelicula.empty:
        return f"Película no encontrada"

    #Acceder al primer elemento para convertir los valores en cadenas de texto y construir el mensaje de salida
    pelicula_nombre = pelicula["title"].iloc[0]
    año_estreno = pelicula["release_year"].iloc[0]
    score = pelicula["vote_average"].iloc[0]

      
    return f"La película {pelicula_nombre} fue estrenada en el año {año_estreno} con un score/popularidad de {score}"

@app.get("/votos_titulo/{Titulo}")

def votos_titulo( titulo_de_la_filmación ):
    '''
    Presenta el título de la película, el año de estreno, la cantidad de votos y el score
    para películas que tuvieron una cantidad mayor de 2000 valoraciones
    argumento
    titulo_de_la_filmación : Título de una filmación
    Devuelve
    Titulo de la filmación, año de estreno, cantidad de votos y promedio de votos
    '''
    #Ir al archivo movies para obtener las películas
    movies = pd.read_csv("Datasets/movies.csv")

    #Colocar todo lo escrito en el titulo en minusculas para facilitar busqueda
    titulo_de_la_filmación = titulo_de_la_filmación.lower()

    #Filtrar las peliculas por el título
    pelicula = movies[movies["title"].str.lower() == titulo_de_la_filmación]
    #Si no se encuentra la película (porque busqueda fue vacía), retornar mensaje:
    if pelicula.empty:
        return f"Película no encontrada"
    
    elif pelicula["vote_count"].iloc[0] < 2000:
        return f"La película no tiene al menos 2000 valoraciones para ser presentada"
    
    #Acceder al primer elemento para convertir los valores en cadenas de texto y construir el mensaje de salida
    pelicula_nombre = pelicula["title"].iloc[0]
    año_estreno = pelicula["release_year"].iloc[0]
    score = pelicula["vote_average"].iloc[0]
    cantidad_votos = pelicula["vote_count"].iloc[0]

    return f" La película {pelicula_nombre} fue estrenada en el año {año_estreno}. La misma cuenta con un total de {cantidad_votos} valoraciones, con un promedio de {score}"


@app.get("/get_actor/{nombre_actor}")

def get_actor( nombre_actor ):
    '''
    Presenta el número de películas en las que ha participado un actor y el promedio de retorno
    Si el actor también es un director, no presenta su información
    argumentos:
    nombre_actor: Nombre de un actor
    Devuelve
    Nombre del actor, número de peliculas en las que ha participado, el retorno total y el retorno promedio por filmación
    '''

    #Ir al archivo de peliculas para obtener la información de las películas

    movies = pd.read_csv("Datasets/movies.csv")

    # Ir al archivo cast para obtener los actores
    cast = pd.read_csv("Datasets/cast.csv")

    #Ir al archivo crew para obtener los directores

    crew = pd.read_csv("Datasets/crew.csv")

    #Filtrar por los directores

    crew_director = crew[crew["job"] == "Director"]

    # Colocar el nombre del actor en minusculas para facilitar la busqueda

    nombre_actor = nombre_actor.lower()

    #Filtramos el archivo de actores por el nombre del actor
    part_actor = cast[cast["name"].str.lower() == nombre_actor]

    #Si no se encuentra el actor devuelve el mensaje:

    if part_actor.empty:
        return"El actor no existe"
    
    #Si el actor también es director, no se tiene en cuenta en la consulta, por lo que no se despliega el siguiente mensaje:

    elif nombre_actor in crew_director["name"].str.lower().values:
        return "El actor también es director por lo que no se presentará su información"
    

    #Se unifica con movies para obtener el return total y promedio
    part_actor = pd.merge(part_actor, movies[["id","return"]], left_on="id_film", right_on="id", how="left")

    total_peliculas = part_actor["id_film"].nunique()
    retorno_total = part_actor["return"].sum()
    retorno_promedio = part_actor["return"].mean()

    return f"El actor {nombre_actor} ha participado de {total_peliculas} cantidad de filmaciones, el mismo ha conseguido un retorno de {retorno_total} con un promedio de {retorno_promedio} por filmación"

@app.get("/get_director/{nombre_director}")

def get_director( nombre_director ):
    '''
    Presenta el nombre del director, su retorno
    Una lista de sus películas drigidas con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma
    argumentos:
    nombre_director: El nombre del director
    Devuelve:
    Nombre del director y su retorno total
    dict: Nombre película, fecha de lanzamiento, retorno individual, costo y ganancia
    '''
    #Ir al archivo de peliculas para obtener la información de las películas

    movies = pd.read_csv("Datasets/movies.csv")

    #Ir al archivo crew para obtener los directores

    crew = pd.read_csv("Datasets/crew.csv")

    #Filtrar por los directores
    crew_director = crew[crew["job"] == "Director"]

    #Convertir nombre de director a minusculas para facilitar la búsqueda
    nombre_director = nombre_director.lower()

    #Filtrar por el nombre del director
    crew_dir_buscado = crew_director[crew_director["name"].str.lower() == nombre_director]

    #Si no se encuentra el director, devuelve el siguiente mensaje:
    if crew_dir_buscado.empty:
        return "El director no existe"
    
    #Se obtiene la información sobre la pelícual: titulo, año estreno, retorno, presupuesto, ganancias:
    crew_dir_buscado = pd.merge(crew_dir_buscado, movies[["id", "title", "release_year", "return", "budget", "revenue"]] , left_on="id_film" , right_on="id", how="left")

    crew_dir_buscado = crew_dir_buscado[["title", "release_year", "return", "budget", "revenue"]]
    retorno_total = crew_dir_buscado["return"].sum()

    resultado = {"El director": nombre_director, "ha tenido un retorno total de": retorno_total, 
                 "estas son sus películas": crew_dir_buscado.reset_index().to_dict(orient="records")}
    return JSONResponse(content=jsonable_encoder(resultado), media_type="application/json")

def obtener_recomendacion (dataset, Titulo:str):
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
        movies = pd.read_csv("Datasets/movies.csv")


        #Aplicar función
        resultado = obtener_recomendacion(movies, Titulo)
        return JSONResponse(content=jsonable_encoder(resultado), media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")
