import re
import json
import logging
from collections import Counter
from typing import List, Tuple

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def q3_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Procesa un archivo NDJSON para contar las menciones de usuarios en los tweets,
    optimizando el tiempo de ejecución.

    Args:
        file_path (str): Ruta del archivo NDJSON.

    Returns:
        List[Tuple[str, int]]: Lista de los 10 usuarios más mencionados con sus frecuencias.
    """
    # Compilar la expresión regular para mejorar el rendimiento
    username_pattern = re.compile(r'@(\w+)')

    # Inicializar el contador de nombres de usuario
    username_counter = Counter()

    try:
        # Abrir el archivo en modo lectura
        with open(file_path, 'r') as file:
            # Usar una expresión generadora para reducir accesos a estructuras
            tweets_content = (
                json.loads(line).get('content', '') for line in file
            )

            # Actualizar el contador en un solo paso para optimizar la velocidad
            for content in tweets_content:
                try:
                    # Encontrar y contar los nombres de usuario en cada contenido
                    mentions = username_pattern.findall(content)
                    if mentions:
                        username_counter.update(mentions)
                except Exception as e:
                    # Registrar cualquier error inesperado
                    logger.warning(f"Error al procesar menciones: {e}")

    except (FileNotFoundError, IOError) as e:
        # Registrar error si no se puede abrir el archivo
        logger.error(f"Error al abrir el archivo: {e}")
        raise
    except json.JSONDecodeError as e:
        # Registrar error si una línea no se puede decodificar
        logger.error(f"Error al decodificar JSON: {e}")
        raise

    # Obtener los 10 usuarios más mencionados
    top_users = username_counter.most_common(10)

    # Registrar los resultados obtenidos
    logger.info(f"Top 10 usuarios mencionados: {top_users}")

    return top_users
