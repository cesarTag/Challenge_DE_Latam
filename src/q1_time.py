import json
import logging
from datetime import datetime
from typing import List, Tuple, Generator, Dict
from collections import defaultdict, Counter

# Configuración del logger
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def leer_tweets(file_path: str) -> Generator[Dict, None, None]:
    """
    Lee el archivo NDJSON línea por línea y genera objetos JSON mediante un generador.

    Args:
        file_path (str): Ruta del archivo NDJSON.

    Yields:
        Dict: Un tweet decodificado como objeto JSON.

    Raises:
        IOError: Si hay problemas al abrir el archivo.
        JSONDecodeError: Si el contenido del archivo no es válido JSON.
    """
    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as e:
                    logger.warning(f"Error al decodificar JSON: {e}")
    except (FileNotFoundError, IOError) as e:
        logger.error(f"Error al abrir el archivo: {e}")
        raise


def map_tweets(tweets: Generator[Dict, None, None]) -> Tuple[Counter, defaultdict]:
    """
    Mapea los tweets para generar contadores de tweets por fecha y usuario.

    Args:
        tweets (Generator): Generador de tweets en formato JSON.

    Returns:
        Tuple[Counter, defaultdict]: Contadores de tweets por fecha y usuarios por fecha.

    Raises:
        KeyError: Si falta información clave en el tweet.
    """
    # Inicialización de contadores
    date_counts = Counter()
    date_user_counts = defaultdict(lambda: defaultdict(int))

    # Procesamiento de cada tweet
    for tweet in tweets:
        try:
            # Extracción de fecha y usuario
            date = datetime.strptime(tweet['date'][:10], "%Y-%m-%d").date()
            user = tweet['user']['username']

            # Actualización de contadores
            date_counts[date] += 1
            date_user_counts[date][user] += 1

        except KeyError as e:
            # Advertencia si falta información clave en el tweet
            logger.warning(f"Tweet malformado, falta información: {e}")

    return date_counts, date_user_counts


def reduce_tweets(
        date_counts: Counter, date_user_counts: defaultdict
) -> List[Tuple[datetime.date, str]]:
    """
    Reduce los contadores para encontrar las 10 fechas más activas y
    los usuarios más frecuentes en cada fecha.

    Args:
        date_counts (Counter): Contador de tweets por fecha.
        date_user_counts (defaultdict): Contador de usuarios por fecha.

    Returns:
        List[Tuple[datetime.date, str]]: Las 10 fechas más activas y
        los usuarios más frecuentes.
    """
    # Obtener las 10 fechas con más tweets
    top_10_dates = date_counts.most_common(10)

    # Construir la lista de resultados
    result = [
        (date, max(date_user_counts[date].items(), key=lambda x: x[1])[0])
        for date, _ in top_10_dates
    ]

    return result


def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Función principal que coordina las fases de Map y Reduce para resolver Q1.

    Args:
        file_path (str): Ruta del archivo NDJSON.

    Returns:
        List[Tuple[datetime.date, str]]: Las 10 fechas más activas y sus usuarios más frecuentes.

    Raises:
        ValueError: Si el path del archivo es nulo o vacío.
    """
    if not file_path:
        logger.error("El path no debe ser nulo o vacío.")
        raise ValueError("El path no debe ser nulo o vacío.")

    # Fase Map: Leer y mapear tweets
    tweets = leer_tweets(file_path)
    date_counts, date_user_counts = map_tweets(tweets)

    # Fase Reduce: Reducir los resultados
    result = reduce_tweets(date_counts, date_user_counts)

    # Registrar el resultado final
    logger.info(f"Proceso completado con éxito. Top 10 fechas: {result}")

    return result
