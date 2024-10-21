import polars as pl
from typing import List, Tuple
from datetime import date


def q1_memory_polars(file_path: str) -> List[Tuple[date, str]]:
    # Validar el path
    if not file_path:
        raise ValueError("El path no debe ser nulo o vacío")

    # Cargar el archivo usando Polars con ejecución lazy
    try:
        data = (
            pl.read_ndjson(file_path, ignore_errors=True)
            .lazy()
            .select([
                pl.col('date').str.slice(0, 10).str.strptime(pl.Date).alias('date'),
                pl.col('user').struct.field('username')
                    .str.to_lowercase()
                    .str.replace_all(' ', '')
                    .alias('username')
            ])
            .filter(pl.col('username').is_not_null())
        )
    except (FileNotFoundError, IOError) as e:
        print(f"Error al abrir el archivo en {file_path}: {e}")
        raise

    # Agrupar y contar tweets por fecha y usuario
    df_conteo_tweets = (
        data.group_by(['date', 'username'])
        .agg(pl.len().alias('tweets'))
    )

    # Obtener la suma total de tweets por fecha
    sum_tweets_data = (
        df_conteo_tweets.group_by('date')
        .agg(pl.col('tweets').sum().alias('sum_tweets'))
    )

    # Obtener el usuario con más tweets por fecha
    top_twitters_df = (
        df_conteo_tweets.sort(by=['date', 'tweets'], descending=[False, True])
        .group_by('date')
        .first()
    )

    # Unir ambos DataFrames
    df_final = (
        top_twitters_df.join(sum_tweets_data, on='date')
        .sort('sum_tweets', descending=True)
    )

    # Materializar el DataFrame y obtener los resultados como lista de tuplas
    resultado = df_final.select(['date', 'username']).limit(10).collect().to_numpy().tolist()

    return resultado
