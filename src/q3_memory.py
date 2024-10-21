import re
import json
import logging
from collections import Counter
from typing import List, Tuple

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Procesa un archivo NDJSON para contar las menciones de usuarios en los tweets,
    optimizando el uso de memoria.

    Args:
        file_path (str): Ruta del archivo NDJSON.

    Returns:
        List[Tuple[str, int]]: Lista de los 10 usuarios más mencionados con sus frecuencias.
    """
    # Compilar la expresión regular para encontrar menciones (@usuario)
    username_pattern = re.compile(r'@(\w+)')

    # Inicializar el contador para los nombres de usuario
    mention_counter = Counter()

    try:
        # Abrir el archivo y procesar línea por línea (minimiza uso de memoria)
        with open(file_path, 'r') as tweet_file:
            for tweet_json in tweet_file:
                try:
                    # Parsear la línea como JSON
                    tweet_data = json.loads(tweet_json.strip())
                except json.JSONDecodeError as e:
                    # Registrar advertencia y continuar con la siguiente línea
                    logger.warning(f"Error al decodificar JSON: {e}")
                    continue

                # Extraer el contenido del tweet si está disponible
                tweet_content = tweet_data.get('content', '')

                # Encontrar todas las menciones de usuario en el contenido
                mentioned_users = username_pattern.findall(tweet_content)

                # Actualizar el contador solo si hay menciones
                if mentioned_users:
                    mention_counter.update(mentioned_users)

    except (FileNotFoundError, IOError) as e:
        # Registrar error si el archivo no se encuentra o no se puede abrir
        logger.error(f"Error al abrir el archivo: {e}")
        raise

    # Obtener los 10 usuarios más mencionados
    top_mentioned_users = mention_counter.most_common(10)

    # Registrar los usuarios más mencionados
    logger.info(f"Top 10 usuarios mencionados: {top_mentioned_users}")

    return top_mentioned_users
