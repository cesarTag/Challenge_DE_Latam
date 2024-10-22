import json
import logging
from datetime import datetime
from typing import List, Tuple, Generator, Dict
from collections import Counter, defaultdict

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def leer_tweets(file_path: str) -> Generator[Dict, None, None]:
    """
    Lee el archivo NDJSON línea por línea y genera objetos JSON.

    Args:
        file_path (str): Ruta del archivo NDJSON.

    Yields:
        Dict: Un tweet decodificado como objeto JSON.

    Raises:
        IOError: Si hay problemas al abrir el archivo.
        json.JSONDecodeError: Si el contenido del archivo no es válido JSON.
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
    Procesa los tweets y genera contadores de tweets por fecha y usuarios por fecha.

    Args:
        tweets (Generator): Generador de tweets en formato JSON.

    Returns:
        Tuple[Counter, defaultdict]: Contador de tweets por fecha y usuarios por fecha.

    Raises:
        KeyError: Si falta información clave en el tweet.
    """
    date_counts = Counter()
    date_user_counts = defaultdict(Counter)

    for tweet in tweets:
        try:
            # Extracción de datos
            date = datetime.strptime(tweet['date'][:10], "%Y-%m-%d").date()
            user = tweet['user']['username']

            # Actualización de contadores
            date_counts[date] += 1
            date_user_counts[date][user] += 1
        except KeyError as e:
            logger.warning(f"Tweet malformado, falta información: {e}")

    return date_counts, date_user_counts


def reduce_tweets(
        date_counts: Counter, date_user_counts: defaultdict
) -> List[Tuple[datetime.date, str]]:
    """
    Reduce los contadores para obtener las 10 fechas con más tweets y el usuario más activo en cada una.

    Args:
        date_counts (Counter): Contador de tweets por fecha.
        date_user_counts (defaultdict): Contador de usuarios por fecha.

    Returns:
        List[Tuple[datetime.date, str]]: Lista de las 10 fechas con más tweets y su usuario más activo.
    """
    # Obtener las 10 fechas con más tweets
    top_10_dates = date_counts.most_common(10)

    # Construcción del resultado
    result = [
        (date, date_user_counts[date].most_common(1)[0][0])
        for date, _ in top_10_dates
    ]

    return result


def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Implementación modular de la solución Q1 utilizando MapReduce para optimizar el uso de memoria.

    Args:
        file_path (str): Ruta del archivo NDJSON.

    Returns:
        List[Tuple[datetime.date, str]]: Lista de las 10 fechas con más tweets y el usuario más activo en cada una.

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

    logger.info(f"Proceso completado con éxito. Top 10 fechas: {result}")
    return result
