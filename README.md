En este repositorio se encuentra la Solución al Laboratorio 1

Primer paso:
Se realizo el proceso de ETL solicitado, el cual se encuentra descrito en el archivo que tiene por nombre ETL
ETL.ipynb


Segundo paso:
Se realizo la creación de las apis con el uso de FastAPI y disponible en web a través de Render para ser consultadas
La dirección publica es: https://solucion-laboratorio-1-saray-pacheco.onrender.com
Cada función tiene su decorador:
def cantidad_filmaciones_mes( Mes ): @app.get("/cantidad_filmaciones_mes/{Mes}")
def cantidad_filmaciones_dia( Dia ): @app.get("/cantidad_filmaciones_dia/{Dia}")
def score_titulo( titulo_de_la_filmación ): @app.get("/score_titulo/{Titulo}")
def votos_titulo( titulo_de_la_filmación ): @app.get("/votos_titulo/{Titulo}")
def get_actor( nombre_actor ): @app.get("/get_actor/{nombre_actor}")
def get_director( nombre_director ): @app.get("/get_director/{nombre_director}")

Tercer paso
Se realiza un análisi exploratorio de los datos, el cual se encuentra descrito paso a paso en el archivo que tiene por nombre EDA.ipyn

Cuarto paso
Se realizo la creación del sistema de recomendación utilizando la similitud del coseno, también se creo una función para consultarla a través de FastAPI y disponible en web en Reder
@app.get("/recomendacion/{titulo}")
