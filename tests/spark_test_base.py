import unittest
from pyspark.sql import SparkSession
import os

# Ajuste para Windows (se necessário)
os.environ["PYSPARK_PYTHON"] = "python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python"

class SparkTestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder \
            .master("local[*]") \
            .appName("PySpark Unit Tests") \
            .getOrCreate()

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()
