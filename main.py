from fastapi import FastAPI, HTTPException
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import locale

app = FastAPI()

# Establecer el idioma local a español para hacer las consultas en español
locale.setlocale(locale.LC_TIME, 'es_ES')

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
    movies = pd.read_csv(r"C:\Users\SARAY\Documents\Cursos Cortos\Henry\Laboratorios Individual\Laboratorio 1\Solucion Laboratorio 1\Datasets\movies.csv")
    # Se Convierte la columna de release_date
    movies["release_date"] = pd.to_datetime(movies["release_date"])
    #Incluir una columna con el nombre del mes en español
    mes_Español = {1:"enero", 2:"febrero", 3:"marzo", 4:"abril", 5:"mayo", 6:"junio", 7:"julio", 8:"agosto", 
               9:"septiembre", 10:"octubre", 11:"noviembre", 12:"diciembre"}
    movies["mes_estreno"] = movies["release_date"].dt.month.map(mes_Español)
    movies["mes_estreno"] = movies["mes_estreno"].astype("string")
    
    #Obtener la cantidad de peliculas en el mes
    movies_pormes = movies[movies["mes_estreno"] == Mes.lower()].shape[0]

    return f"{movies_pormes} cantidad de películas fueron estrenadas en el mes de {Mes}"