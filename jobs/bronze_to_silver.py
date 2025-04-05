from pyspark.sql import SparkSession
import time
from pyspark.sql.functions import col
from dotenv import load_dotenv
import os

class SilverLayerProcessor:
    def __init__(self, spark: SparkSession, input_path: str, output_path: str):
        self.spark = spark
        self.input_path = input_path
        self.output_path = output_path

    def read_data(self):
        return self.spark.read.json(self.input_path)

    def transform_data(self, df): # facilitate users filters
        return df.filter(col("state").isNotNull() & col("city").isNotNull())
            
    def write_data(self, df):
        df.write.mode("overwrite").partitionBy("state", "city").parquet(self.output_path)

    def process(self):
        df = self.read_data()
        df.show(truncate=False)
        df_transformed = self.transform_data(df)
        print("Socorro")
        df_transformed.show()
        self.write_data(df_transformed)


if __name__ == "__main__":
    # Carrega as variáveis do arquivo .env
    load_dotenv()

    # Pega as variáveis do ambiente
    endpoint = os.getenv("MINIO_ENDPOINT")
    access_key = os.getenv("MINIO_ACCESS_KEY")
    secret_key = os.getenv("MINIO_SECRET_KEY")

    # Cria a sessão Spark com configurações S3A para MinIO
    spark = (
        SparkSession.builder
        .appName("SilverLayerProcessor")
        .config("spark.hadoop.fs.s3a.endpoint", f"http://{endpoint}")
        .config("spark.hadoop.fs.s3a.access.key", access_key)
        .config("spark.hadoop.fs.s3a.secret.key", secret_key)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.1")
        .getOrCreate()
    )

    processor = SilverLayerProcessor(
        spark,
        input_path="s3a://beer-data-lake/bronze/breweries/*.json",
        output_path="s3a://beer-data-lake/silver/brewery_data/"
    )

    processor.process()
    time.sleep(5)  # dá tempo do Spark imprimir os dados
    spark.stop()
