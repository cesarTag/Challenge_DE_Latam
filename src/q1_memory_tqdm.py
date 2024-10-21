from collections import Counter, defaultdict
from datetime import datetime
import json
from tqdm.contrib.concurrent import process_map


# Función para procesar cada línea
def process_line(line):
    date_counts = Counter()
    date_user_counts = {}
    tweet = json.loads(line)
    date = datetime.fromisoformat(tweet['date'].replace('Z', '+00:00')).date()
    user = tweet['user']['username']
    return date, user

def file_line_iterator(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield line

def file_all_lines(file_path):
    # Leer todas las líneas del archivo
    with open(file_path, 'r') as file:
        return file.readlines()



def q1_memory_tqdm(file_path, load_file='full'):
    
    #conteo de tweets por fecha
    date_counts = Counter()
    #conteo tweets por fecha y usuario
    date_user_counts = defaultdict(Counter)
    
    if load_file == 'full':
      lines = file_all_lines(file_path)
    else:
      lines = file_line_iterator(file_path)

    # Procesar las líneas en paralelo
    results = process_map(process_line, lines, chunksize=5000, desc="Procesando Lineas")

    #para cada usuario y fecha
    for date, user in results:
        date_counts[date] += 1
        date_user_counts[date][user] += 1
    
    #las 10 fechas con mas tweets
    top_10_dates = date_counts.most_common(10)

    resultado = [(date, date_user_counts[date].most_common(1)[0][0])
                                                    for date, _ in top_10_dates]
    #retorna el resultado ordenado por el campo date
    return resultado
