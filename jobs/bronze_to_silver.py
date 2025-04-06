from pyspark.sql import SparkSession
from pyspark.sql.functions import col

class SilverLayerProcessor:
    def __init__(self, spark: SparkSession, input_path: str, output_path: str):
        self.spark = spark
        self.input_path = input_path
        self.output_path = output_path

    def read_data(self):
        return self.spark.read.json(self.input_path)

    def filter_data_by_state_and_city_not_null(self, df):
        return df.filter(col("state").isNotNull() & col("city").isNotNull())
            
    def write_data(self, df):
        df.write.mode("overwrite").partitionBy("state", "city").parquet(self.output_path)

    def run_pipeline(self):
        df = self.read_data()
        df_filtered = self.filter_data_by_state_and_city_not_null(df)
        self.write_data(df_filtered)
