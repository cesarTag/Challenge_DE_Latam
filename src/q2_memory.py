import json
import logging
from collections import Counter
from typing import List, Tuple
import emoji

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Procesa un archivo NDJSON en streaming para contar las ocurrencias de emojis
    en los tweets, optimizando el uso de memoria.

    Args:
        file_path (str): Ruta del archivo NDJSON.

    Returns:
        List[Tuple[str, int]]: Lista de los 10 emojis más comunes con sus frecuencias.
    """
    # Inicializar un contador para los emojis
    emojis = Counter()

    try:
        # Procesar el archivo línea por línea para minimizar el uso de memoria
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    # Decodificar cada línea del archivo como JSON
                    tweet = json.loads(line)
                except json.JSONDecodeError as e:
                    # Registrar el error y continuar con la siguiente línea
                    logger.warning(f"Error al decodificar JSON: {e}")
                    continue

                # Extraer el contenido del tweet y buscar emojis
                content = tweet.get('content', '')
                emojis_ = emoji.emoji_list(content)

                # Actualizar el contador solo si se encuentran emojis
                if emojis_:
                    emojis.update(emo['emoji'] for emo in emojis_)

    except (FileNotFoundError, IOError) as e:
        # Registrar error si el archivo no se encuentra o no se puede abrir
        logger.error(f"Error al abrir el archivo: {e}")
        raise

    # Devolver los 10 emojis más comunes
    return emojis.most_common(10)
