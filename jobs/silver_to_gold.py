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
        return (df.groupBy("state", "city", "brewery_type")
                .agg(f.count("*").alias("brewery_count")))

    def write_data(self, df):
        (df.write
           .format("parquet")
           .mode("overwrite")
           .save(self.output_path))

    def process(self):
        df = self.read_data()
        df_aggregated = self.aggregate_data(df)
        self.write_data(df_aggregated)


if __name__ == "__main__":
    spark = (SparkSession.builder
         .appName("GoldLayerAggregator")
        #  .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
         .config("spark.hadoop.fs.s3a.access.key", "minioadmin")  # ou outro usuário configurado
         .config("spark.hadoop.fs.s3a.secret.key", "minioadmin")  # ou a senha correspondente
         .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")  # ajuste se o hostname for diferente
         .config("spark.hadoop.fs.s3a.path.style.access", "true")
         .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
         .getOrCreate())

    aggregator = GoldLayerAggregator(
        spark,
        input_path="s3a://beer-data-lake/silver/brewery_data/",
        output_path="s3a://beer-data-lake/gold/breweries_aggregated/"
    )

    aggregator.process()
    spark.stop()