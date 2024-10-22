import re
import json
import logging
from collections import Counter
from typing import List, Tuple, Generator, Dict

# Configuración del logger
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def leer_tweets(file_path: str) -> Generator[Dict, None, None]:
    """
    Lee el archivo NDJSON línea por línea y genera objetos JSON.

    Args:
        file_path (str): Ruta del archivo NDJSON.

    Yields:
        Dict: Tweet decodificado como objeto JSON.

    Raises:
        FileNotFoundError: Si el archivo no se encuentra.
        IOError: Si hay problemas al abrir el archivo.
    """
    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    yield json.loads(line.strip())
                except json.JSONDecodeError as e:
                    logger.warning(f"Error al decodificar JSON: {e}")
    except (FileNotFoundError, IOError) as e:
        logger.error(f"Error al abrir el archivo: {e}")
        raise


def map_mentions(tweets: Generator[Dict, None, None]) -> Counter:
    """
    Mapea los tweets para extraer y contar menciones de usuarios.

    Args:
        tweets (Generator): Generador de tweets en formato JSON.

    Returns:
        Counter: Contador con las ocurrencias de cada usuario mencionado.
    """
    username_pattern = re.compile(r'@(\w+)')
    mention_counter = Counter()

    for tweet in tweets:
        content = tweet.get('content', '')
        mentioned_users = username_pattern.findall(content)
        if mentioned_users:
            mention_counter.update(mentioned_users)

    return mention_counter


def reduce_mentions(mention_counters: List[Counter]) -> Counter:
    """
    Reduce los contadores de menciones para obtener el total de ocurrencias.

    Args:
        mention_counters (List[Counter]): Lista de contadores de menciones.

    Returns:
        Counter: Contador combinado con las ocurrencias totales.
    """
    total_counter = Counter()
    for counter in mention_counters:
        total_counter.update(counter)
    return total_counter


def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Función principal que coordina las fases de Map y Reduce para contar menciones de usuarios.

    Args:
        file_path (str): Ruta del archivo NDJSON.

    Returns:
        List[Tuple[str, int]]: Lista de los 10 usuarios más mencionados con sus frecuencias.

    Raises:
        ValueError: Si el path del archivo es nulo o vacío.
    """
    if not file_path:
        logger.error("El path no debe ser nulo o vacío.")
        raise ValueError("El path no debe ser nulo o vacío.")

    tweets = leer_tweets(file_path)
    mention_counter = map_mentions(tweets)

    result = mention_counter.most_common(10)

    logger.info(f"Top 10 usuarios mencionados: {result}")

    return result
