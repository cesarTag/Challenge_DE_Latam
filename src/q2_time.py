import json
import logging
from collections import Counter
from typing import List, Tuple, Generator, Dict
import emoji

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
        FileNotFoundError: Si el archivo no se encuentra.
        IOError: Si hay problemas al abrir el archivo.
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


def map_emojis(tweets: Generator[Dict, None, None]) -> Counter:
    """
    Mapea los tweets para extraer y contar emojis.

    Args:
        tweets (Generator): Generador de tweets en formato JSON.

    Returns:
        Counter: Contador con las ocurrencias de cada emoji.
    """
    emoji_counter = Counter()

    for tweet in tweets:
        content = tweet.get('content', '')
        emojis_ = emoji.emoji_list(content)

        if emojis_:
            emoji_counter.update(emo['emoji'] for emo in emojis_)

    return emoji_counter


def reduce_emojis(emoji_counters: List[Counter]) -> Counter:
    """
    Reduce los contadores para obtener las ocurrencias totales de cada emoji.

    Args:
        emoji_counters (List[Counter]): Lista de contadores de emojis.

    Returns:
        Counter: Contador combinado con las ocurrencias totales de cada emoji.
    """
    total_counter = Counter()
    for counter in emoji_counters:
        total_counter.update(counter)
    return total_counter


def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Función principal que coordina las fases de Map y Reduce para contar emojis.

    Args:
        file_path (str): Ruta del archivo NDJSON.

    Returns:
        List[Tuple[str, int]]: Lista de los 10 emojis más comunes con sus frecuencias.

    Raises:
        ValueError: Si el path del archivo es nulo o vacío.
    """
    if not file_path:
        logger.error("El path no debe ser nulo o vacío.")
        raise ValueError("El path no debe ser nulo o vacío.")

    tweets = leer_tweets(file_path)
    emoji_counter = map_emojis(tweets)

    # Reducir resultados (en esta implementación no hay múltiples contadores)
    result = emoji_counter.most_common(10)

    logger.info(f"Proceso completado. Top 10 emojis: {result}")

    return result
