from typing import List, Tuple
from datetime import datetime
from pyspark.sql.functions import to_date, col, sum, rank, when, col, regexp_replace, lower
from pyspark.sql.window import Window
import findspark
from pyspark.sql import SparkSession


def getSparkInstance(name_app="test_app") -> SparkSession:
    findspark.init()
    spark = SparkSession.builder \
      .appName(name_app) \
      .config("spark.driver.memory", "4g") \
      .config("spark.executor.extraJavaOptions", "--illegal-access=permit") \
      .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def q1_memory_pyspark(file_path: str) -> List[Tuple[datetime.date, str]]:
	# validate path
  if not file_path:
    raise ValueError("El path no debe ser nulo o vacío")
  
  spark = getSparkInstance("q1_memory_app")
  data = None
  # Se leen solo las columnas necesarias para reducir el uso de memoria, se formatea solo a fecha el campo datetime
  try:
    data = spark.read.json(file_path).select('date', 'user.username') \
      .withColumn("date", to_date("date")) \
      .withColumn("username", when(col("username").isNotNull(), regexp_replace(lower('username'), ' ', '')).otherwise(None))
  except (FileNotFoundError, IOError) as e:
    print(f'Problema al encontrar el archivo en esta ubicacion {file_path}, error -> {e}')
  # Se convierte la columna 'date' a solo la fecha
  df_conteo_tweets = data.groupBy('date', 'username').count().withColumnRenamed("count", "tweets")

	# Ventana para setear al usuario con mas tweets de forma descendente
  window = Window.partitionBy('date').orderBy(col('tweets').desc())
	# asignar un numero de fila a cada uno sobre cada ventana de fecha ordenados por tweets en forma descendiente
  top_twitters_df = df_conteo_tweets.withColumn('top_twitters', rank().over(window)).filter(col('top_twitters') == 1)
	# creamos dataframe con la suma de tweets por fecha
  max_tweets_data = df_conteo_tweets.groupBy("date").agg(sum("tweets").alias("sum_tweets"))
  df_final = top_twitters_df.join(max_tweets_data, "date", "inner").select('*').orderBy(col('sum_tweets').desc())
	# Se retorna una tupla con el resultado
  resultado = [(row['date'], row['username']) for row in df_final.collect()]
  spark.stop()
  return resultado
