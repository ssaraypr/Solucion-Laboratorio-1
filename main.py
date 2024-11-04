from fastapi import FastAPI, HTTPException
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

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
