from pyspark.sql import SparkSession
from pyspark.sql import functions as f


class GoldLayerAggregator:
    def __init__(self, spark: SparkSession, input_path: str, output_path: str):
        self.spark = spark
        self.input_path = input_path
        self.output_path = output_path

    def read_data(self):
        return self.spark.read.format("parquet").load(self.input_path)

    def aggregate_data(self, df):
        return (
            df.groupBy("state", "city", "brewery_type")
            .agg(f.count("*").alias("brewery_count"))
        )

    def write_data(self, df): (
        df.write
        .format("parquet")
       .mode("overwrite")
       .save(self.output_path)
    )

    def run_pipeline(self):
        df = self.read_data()
        df_aggregated = self.aggregate_data(df)
        self.write_data(df_aggregated)
