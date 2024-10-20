import json
import logging
from datetime import datetime
from typing import List, Tuple
from collections import Counter, defaultdict

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def q1_memory_optimized_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Procesa un archivo NDJSON línea por línea, contando la cantidad de tweets por fecha
    y por usuario, optimizando el uso de memoria con generadores.

    Args:
        file_path (str): Ruta del archivo NDJSON.

    Returns:
        List[Tuple[datetime.date, str]]: Lista de las 10 fechas con más tweets
        y el usuario más activo en cada una.
    """
    if not file_path:
        logger.error("El path no debe ser nulo o vacío.")
        raise ValueError("El path no debe ser nulo o vacío.")

    date_counts = Counter()
    date_user_counts = defaultdict(Counter)

    # Generador que procesa las líneas del archivo para minimizar el uso de memoria
    def tweet_generator(file):
        try:
            for line in file:
                yield json.loads(line)
        except json.JSONDecodeError as e:
            logger.error(f"Error al decodificar JSON: {e}")
            raise

    try:
        with open(file_path, 'r') as file:
            for tweet in tweet_generator(file):
                # Extracción de datos
                date = datetime.strptime(tweet['date'][0:10], "%Y-%m-%d").date()
                user = tweet['user']['username']

                # Actualización de contadores
                date_counts[date] += 1
                date_user_counts[date][user] += 1

        # Obtener las 10 fechas con más tweets
        top_10_dates = date_counts.most_common(10)

        # Construcción del resultado con list comprehension
        result = [
            (date, date_user_counts[date].most_common(1)[0][0])
            for date, _ in top_10_dates
        ]

        return result

    except (FileNotFoundError, IOError) as e:
        logger.error(f"Error al abrir el archivo: {e}")
        raise
