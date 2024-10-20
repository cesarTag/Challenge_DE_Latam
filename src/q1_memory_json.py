import json
from datetime import datetime
from typing import List, Tuple
from collections import Counter, defaultdict

def q1_memory_json(file_path: str) -> List[Tuple[datetime.date, str]]:

    if not file_path:
      raise ValueError("El path no debe ser nulo o vacío")
    # Uso de defaultdict para evitar comprobaciones explícitas de existencia
    date_counts = Counter()
    date_user_counts = defaultdict(Counter)

    # Abrir el archivo y procesar línea por línea (evita cargar todo en memoria)
    with open(file_path, 'r') as file:
        for line in file:
            tweet = json.loads(line)
            date = datetime.strptime(tweet['date'][0:10], "%Y-%m-%d").date()
            user = tweet['user']['username']

            # Actualizar contadores
            date_counts[date] += 1
            date_user_counts[date][user] += 1

    # Obtener las 10 fechas con más tweets
    top_10_dates = date_counts.most_common(10)

    # Crear el resultado usando list comprehension
    result = [
        (date, date_user_counts[date].most_common(1)[0][0])
        for date, _ in top_10_dates
    ]

    # Retornar la lista ordenada por fecha
    return result
