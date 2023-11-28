from fastapi import FastAPI, HTTPException
import pandas as pd






app = FastAPI()

ruta_archivo = 'Data/genero_play_time.parquet'  
horas_usuario = pd.read_parquet(ruta_archivo)

@app.get("/PlayTimeGenre/{genero}")
async def PlayTimeGenre(genero: str):
    """
    Obtén el año con más horas jugadas para un género específico.

    Parámetros:
    - genero (str): Género para el cual se desea obtener el año con más horas jugadas.

    Ejemplo de uso:
    - /PlayTimeGenre/Action

    Retorna:
    - dict: {"Año con más horas jugadas para el género": genero, "Año": max_playtime_year}
    """
    df_genero = horas_usuario[horas_usuario['genres'].str.contains(genero, na=False)]
  
    df_grouped = df_genero.groupby('Año_estreno')['playtime_forever'].sum()
    
    max_playtime_year = df_grouped.idxmax()
    
    return {"Año con más horas jugadas para el género": genero, "Año": max_playtime_year}





df_horas_usuario = pd.read_parquet('Data/user_for_genero_mitad.parquet')

@app.get("/UserForGenre/{genero}")
async def UserForGenre(genero: str):
    """
    Obtén información sobre el usuario con más horas jugadas y la acumulación de horas jugadas por año para un género específico.

    Parámetros:
    - genero (str): Género para el cual se desea obtener la información.

    Ejemplo de uso:
    - /UserForGenre/Action

    Retorna:
    - dict: {
        "Usuario con más horas jugadas para Género": usuario_con_mas_horas,
        "Horas jugadas": lista_acumulacion
      }

    Si no hay datos para el género, el mensaje será:
    - {"mensaje": "No hay datos para el género '{genero}'."}
    """
    df_genre = df_horas_usuario[df_horas_usuario['genres'] == genero]

    if df_genre.empty:
        return {"mensaje": f"No hay datos para el género '{genero}'."}

    usuario_con_mas_horas = df_genre.groupby('user_id')['playtime_forever'].sum().idxmax()

    acumulacion_por_anio = df_genre.groupby('Año_estreno')['playtime_forever'].sum().reset_index()
    acumulacion_por_anio = acumulacion_por_anio.rename(columns={"playtime_forever": "Horas"})
    lista_acumulacion = acumulacion_por_anio.to_dict(orient='records')

    salida = {
        "Usuario con más horas jugadas para Género": usuario_con_mas_horas,
        "Horas jugadas": lista_acumulacion
    }

    return salida


recomendado = pd.read_parquet('Data/Recommend_Users2.parquet')

@app.get('/UsersRecommend/{anio}')
async def UsersRecommend(anio: int):
    """
    Obtiene las principales recomendaciones de juegos para un año específico.

    Parámetros:
    - anio (int): Año para el cual se desean obtener las recomendaciones de juegos.

    Ejemplo de uso:
    - /UsersRecommend/2022

    Retorna:
    - list: [
        {"Puesto 1": nombre_juego_1},
        {"Puesto 2": nombre_juego_2},
        {"Puesto 3": nombre_juego_3}
      ]

    Si no hay datos para el año, se lanza una excepción HTTP con código 404.
    Si no hay juegos recomendados para el año, se lanza una excepción HTTP con código 404.
    Si se produce un error inesperado, se lanza una excepción HTTP con código 500.
    """
    try:
        # Filtrar por año
        df_year = recomendado[recomendado['Año_estreno'] == anio]

        # Verificar si hay datos para el año
        if df_year.empty:
            raise HTTPException(status_code=404, detail=f"No hay datos para el año {anio}.")

        # Filtrar recomendaciones positivas
        df_recommendations = df_year[(df_year['recommend'] == True) & (df_year['sentiment_analisis'] >= 1)]

        # Verificar si hay juegos recomendados
        if df_recommendations.empty:
            raise HTTPException(status_code=404, detail=f"No hay juegos recomendados para el año {anio}.")

        # Agrupar por juego y sumar sentimientos
        grouped_games = df_recommendations.groupby('item_name')['sentiment_analisis'].sum()

        # Obtener los tres juegos principales
        top_3_games = grouped_games.nlargest(3)

        # Formatear la salida como una lista de diccionarios
        output_list = [{"Puesto 1": top_3_games.index[0]},
                       {"Puesto 2": top_3_games.index[1]},
                       {"Puesto 3": top_3_games.index[2]}]

        return output_list

    except Exception as e:
        # Manejar errores inesperados con una excepción HTTP 500
        raise HTTPException(status_code=500, detail=f"Se produjo un error inesperado: {str(e)}")

    
df_recomendado = pd.read_parquet('Data/Recommend_Users2.parquet')

@app.get('/UsersWorstDeveloper/{anio}')
async def UsersWorstDeveloper(anio: int):
    """
    Obtiene los juegos menos recomendados por los desarrolladores para un año específico.

    Parámetros:
    - anio (int): Año para el cual se desean obtener los juegos menos recomendados.

    Ejemplo de uso:
    - /UsersWorstDeveloper/2022

    Retorna:
    - list: [
        {"Puesto 1": nombre_juego_1},
        {"Puesto 2": nombre_juego_2},
        {"Puesto 3": nombre_juego_3}
      ]

    Si no hay datos para el año o no hay juegos menos recomendados, se lanza una excepción HTTP con código 404.
    Si se produce un error inesperado, se lanza una excepción HTTP con código 500.
    """
    try:
        # Filtrar por año
        df_year = df_recomendado[df_recomendado['Año_estreno'] == anio]

        # Filtrar juegos menos recomendados
        df_not_recommendations = df_year[(df_year['recommend'] == False) & (df_year['sentiment_analisis'] == 0)]

        # Verificar si hay datos de juegos menos recomendados
        if df_not_recommendations.empty:
            raise HTTPException(status_code=404, detail=f"No hay datos de juegos menos recomendados para el año {anio} con los filtros especificados.")

        # Contar juegos menos recomendados
        juegos_menos_recomendados = df_not_recommendations['item_name'].value_counts().reset_index()
        juegos_menos_recomendados.columns = ['item_name', 'count']

        # Obtener los tres juegos menos recomendados
        top_juegos_menos_recomendados = juegos_menos_recomendados.nlargest(3, 'count')

        # Crear la lista de salida en el formato deseado
        resultado = [{"Puesto 1": top_juegos_menos_recomendados.iloc[0]['item_name']},
                     {"Puesto 2": top_juegos_menos_recomendados.iloc[1]['item_name']},
                     {"Puesto 3": top_juegos_menos_recomendados.iloc[2]['item_name']}]

        return resultado

    except Exception as e:
        # Manejar errores inesperados con una excepción HTTP 500
        raise HTTPException(status_code=500, detail=f"Se produjo un error inesperado: {str(e)}")


analisis_sentimiento = pd.read_parquet('Data/Sentiment.parquet')

@app.get('/sentiment_analysis/{desarrolladora}')
def sentiment_analysis(desarrolladora: str):
    """
    Realiza análisis de sentimiento para una desarrolladora específica.

    Parámetros:
    - desarrolladora (str): Nombre de la desarrolladora para la cual se realiza el análisis de sentimiento.

    Ejemplo de uso:
    - /sentiment_analysis/EjemploDevelopers

    Retorna:
    - dict: {
        "desarrolladora": [
            "Negative = cantidad",
            "Neutral = cantidad",
            "Positive = cantidad"
        ]
      }

    Si no hay datos para la desarrolladora, se devuelve un mensaje indicando la ausencia de datos.
    """
    try:
        # Mapeo de valores de sentimiento
        sentiment_mapping = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}

        # Filtrar por desarrolladora
        df_developer = analisis_sentimiento[analisis_sentimiento['developer'] == desarrolladora]

        # Verificar si hay datos para la desarrolladora
        if df_developer.empty:
            return {desarrolladora: "No hay datos para la desarrolladora."}

        # Mapear los valores de sentimiento
        df_developer['sentiment_analisis'] = df_developer['sentiment_analisis'].map(sentiment_mapping)

        # Contar la frecuencia de cada sentimiento
        sentiment_counts = df_developer['sentiment_analisis'].value_counts().to_dict()

        # Crear la lista de salida en el formato deseado
        output_list = [f"{key} = {value}" for key, value in sentiment_counts.items()]

        return {desarrolladora: output_list}

    except Exception as e:
        # Manejar errores inesperados con una respuesta genérica
        return {"message": f"Se produjo un error inesperado: {str(e)}"}



