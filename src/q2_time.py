import json
import logging
from collections import Counter
from typing import List, Tuple
import emoji

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def q2_memory_emoji_optimized_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Procesa un archivo NDJSON para contar las ocurrencias de emojis en los tweets,
    optimizando el tiempo de ejecución.

    Args:
        file_path (str): Ruta del archivo NDJSON.

    Returns:
        List[Tuple[str, int]]: Lista de los 10 emojis más comunes con sus frecuencias.
    """
    # Inicializar el contador de emojis
    emojis = Counter()

    try:
        # Abrir el archivo en modo lectura
        with open(file_path, 'r') as file:
            # Generador para extraer el contenido de cada tweet
            tweets = (json.loads(line).get('content', '') for line in file)

            # Extraer emojis y actualizar el contador en un solo paso
            for content in tweets:
                try:
                    emojis_ = emoji.emoji_list(content)
                    if emojis_:
                        emojis.update(emo['emoji'] for emo in emojis_)
                except Exception as e:
                    # Registrar cualquier error inesperado
                    logger.warning(f"Error al procesar emojis: {e}")

    except (FileNotFoundError, IOError) as e:
        # Registrar error si no se puede abrir el archivo
        logger.error(f"Error al abrir el archivo: {e}")
        raise

    # Obtener los 10 emojis más comunes
    return emojis.most_common(10)
