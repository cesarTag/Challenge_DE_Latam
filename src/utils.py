from pyspark.sql import SparkSession
import zipfile
import findspark
import os


def getSparkInstance(name_app="test_app") -> SparkSession:
    os.environ["SPARK_HOME"] = "/Users/cesartag/Downloads/spark-3.5.3-bin-hadoop3"
    findspark.init()
    spark = SparkSession.builder \
      .appName(name_app) \
      .config("spark.driver.memory", "2g") \
      .config("spark.executor.extraJavaOptions", "--illegal-access=permit") \
      .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def unzipFiles(zip_path):
    extract_to_directory = '/Users/cesartag/PycharmProjects/Challenge_DE_Latam/data'
    # Create a ZipFile object
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract all the contents into the directory
        zip_ref.extractall(extract_to_directory)

