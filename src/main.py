from utils import unzipFiles, getSparkInstance
from q1_memory import q1_memory
from q2_memory import q2_memory
from q3_memory import q3_memory
import os
from q1_time import q1_time
import cProfile

def getResults(file_path):
	results = {"q1_memory_result": q1_memory(file_path), "q2_memory_result": q2_memory(file_path), "q3_memory_result": q3_memory(file_path)}
	for k, v in results.items():
		print(f"{k}\n{v}\n")


if __name__ == "__main__":
	root_path = os.path.dirname(os.path.abspath(__file__))
	print(root_path)
	data_path = f"../data/tweets.json.zip"
	file_path = "farmers-protest-tweets-2021-2-4.json"
	full_file_path = f"../data/{file_path}"
	print(full_file_path)
	#file_path = '/Users/cesartag/PycharmProjects/Challenge_DE_Latam/data/data_test.json'
	#unzipFiles(data_path)
	getResults(full_file_path)
	#cProfile.run('q1_time(file_path)')
	'''spark = getSparkInstance()
	data = spark.read.json(file_path)
	data.show(10)'''

