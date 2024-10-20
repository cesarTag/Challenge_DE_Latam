import json
import logging
from datetime import datetime
from typing import List, Tuple
from collections import defaultdict, Counter

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Procesa un archivo NDJSON línea por línea, contando la cantidad de tweets por fecha
    y usuario, optimizando el tiempo de ejecución.

    Args:
        file_path (str): Ruta del archivo NDJSON.

    Returns:
        List[Tuple[datetime.date, str]]: Lista de las 10 fechas con más tweets
        y el usuario más activo en cada una.
    """
    if not file_path:
        logger.error("El path no debe ser nulo o vacío.")
        raise ValueError("El path no debe ser nulo o vacío.")

    # Contadores optimizados con defaultdict
    date_counts = Counter()
    date_user_counts = defaultdict(lambda: defaultdict(int))

    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    tweet = json.loads(line)
                except json.JSONDecodeError as e:
                    logger.warning(f"Error al decodificar JSON en una línea: {e}")
                    continue  # Ignorar líneas mal formadas y continuar

                # Extracción de datos
                date = datetime.strptime(tweet['date'][0:10], "%Y-%m-%d").date()
                user = tweet['user']['username']

                # Actualización de contadores
                date_counts[date] += 1
                date_user_counts[date][user] += 1

        # Obtener las 10 fechas con más tweets de manera eficiente
        top_10_dates = date_counts.most_common(10)

        # Construcción del resultado con un bucle optimizado
        result = []
        for date, _ in top_10_dates:
            # Uso de max para encontrar el usuario con más tweets en la fecha
            top_user = max(date_user_counts[date].items(), key=lambda x: x[1])[0]
            result.append((date, top_user))

        return result

    except (FileNotFoundError, IOError) as e:
        logger.error(f"Error al abrir el archivo: {e}")
        raise
