## PI_1-MLOps Juegos Steam - Modelo de recomendación

Proyecto Individual 1 de Machine Learning en bootcamp Henry

### Descripción del proyecto:

El proyecto tiene como objetivo simular la función de un MLOps Engineer, fusionando las responsabilidades de un Data Engineer y un Data Scientist, dentro del entorno de la plataforma de juegos Steam. Abordamos un problema de negocio específico mediante la creación de un Producto Mínimo Viable (MVP), que consta de una API desplegada y un modelo de Machine Learning. Este modelo realiza un análisis de sentimientos basado en los comentarios de los usuarios y proporciona un sistema de recomendación de videojuegos para mejorar la experiencia en la plataforma.

### Archivos para prepar:

Archivos de tipo JSON GZIP:

+ **output_steam_games.json** contiene información sobre los juegos; como nombre de los juegos, editores, dessarrolladores.

+ **australian_users_items.json** contiene información de los juegos que utilizan los usuarios, y el tiempo consumido de cada usuario.

+ **autralian_users_reviews.json** contiene los comentarios de los usuarios sobre los juegos que utilizan , recomendaciones, datos url y user_id.

Diccionario de datos [Dataset](/) 


### Rol Data Engineer:

#### ETL Extracción, Transformación y Carga

Notebooks [ETL](/ETL.ipynb).

En el archivo ETL se lleva a cabo la transformación de los conjuntos de datos, preparando las columnas y filas. Se verifica y ajusta los tipos de datos, y se imputan o eliminan valores faltantes, todo ello con el propósito de preparar los datos para la carga.


#### Análisis Exploratorio de los Datos

Notebook [Analisis exploratorio](/EDA.ipynb)

En el archivo EDA se formulan preguntas de negocio con el objetivo de optimizar los servicios ofrecidos por la plataforma. Se analizan los datos y se buscan correlaciones para lograr la máxima eficiencia, reduciendo costos y maximizando beneficios.

### Desarrollo de Funciones para la API

FastAPI sera la herramienta para desplegar:

def PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.
Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}

def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

def UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

def UsersWorstDeveloper( año : int ): Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

def sentiment_analysis( empresa desarrolladora : str ): Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.
Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}

sistema de recomendación user-item:

def recomendacion_usuario( id de usuario ): Ingresando el id de un usuario, deberíamos recibir una lista con 5 juegos recomendados para dicho usuario.


### Modelamiento (Machine Learning Model Development)

Notebook [Modelo_Recomendacion](/Modelo_Recomendacion.ipynb)

Se crea la matriz de correlacion que representa las correlaciones de los productos mediante la funcion "similitud de coseno" para preparar la funcion "def recomendacion_usuario( id de usuario )".

### FastAPI

Archivo [Main](/main.py). Para ejecutar la API desde localHost seguir los pasos que se detallan acontinuacion:

- Clonar el proyecto haciendo `git clone`.
- Crear el entorno de trabajo en Visual Studio Code:
    * Crear entorno `python -m venv env`
    * Ingresar al entorno haciendo `env\Scripts\activate`
    * Instalar dependencias con `pip install -r requirements.txt`
- Ejecutar el archivo `main.py` desde consola activando uvicorn. Para ello, hacer `uvicorn main:app --reload`
- Hacer Ctrl + clic sobre la dirección `http://XXX.X.X.X:XXXX` (se muestra en la consola).
- Una vez en el navegador, agregar `/docs` para acceder a ReDoc.
- En cada una de las funciones hacer clic en *Try it out* y luego introducir el dato que requiera o utilizar los ejemplos por defecto. Finalmente Ejecutar y observar la respuesta.

### Deploy 

deploy de la API plataforma Render plataforma para crear y ejecutar aplicaciones y sitios web. 

* Se crea un servicio en `render.com`, conectando al repositorio

* Enlace de la aplicacion https://despl.onrender.com/docs

### Video

demostración del funcionamiento de la API [Video](http)

![Pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
![Numpy](https://img.shields.io/badge/-Numpy-333333?style=flat&logo=numpy)
![Matplotlib](https://img.shields.io/badge/-Matplotlib-333333?style=flat&logo=matplotlib)
![Seaborn](https://img.shields.io/badge/-Seaborn-333333?style=flat&logo=seaborn)
![Scikitlearn](https://img.shields.io/badge/-Scikitlearn-333333?style=flat&logo=scikitlearn)
![FastAPI](https://img.shields.io/badge/-FastAPI-333333?style=flat&logo=fastapi)
![TextBlob](https://img.shields.io/badge/-TextBlob-333333?style=flat&logo=textblob)
![Render](https://img.shields.io/badge/-Render-333333?style=flat&logo=render)








