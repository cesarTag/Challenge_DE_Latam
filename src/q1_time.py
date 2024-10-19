from typing import List, Tuple
from datetime import datetime

from utils import getSparkInstance
from pyspark.sql.functions import col, count, date_format, row_number
from pyspark.sql.window import Window

import cProfile


def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    pass
