from prefect import flow
from jobs.ingest_breweries_from_api import (
    BreweryDataPipeline
)
from jobs.bronze_to_silver import (
    SilverLayerProcessor
)
from jobs.silver_to_gold import (
    GoldLayerAggregator
)
from config.spark_session import create_spark_session
from orchestration.prefect.send_webhook_notification import send_webhook_notification

def run_brewery_data_pipeline(bucket_name: str = "beer-data-lake", max_pages: int = 50):
    pipeline = BreweryDataPipeline(bucket_name)
    pipeline.run_pipeline(max_pages=max_pages)

def run_silver_layer_processor(
    input_path: str = "s3a://beer-data-lake/bronze/breweries/*.json",
    output_path: str = "s3a://beer-data-lake/silver/brewery_data/"
):
    spark = create_spark_session("SilverLayerProcessor")
    pipeline = SilverLayerProcessor(spark, input_path, output_path)
    pipeline.run_pipeline()

def run_gold_aggregator(
        input_path: str = "s3a://beer-data-lake/silver/brewery_data/",
        output_path: str = "s3a://beer-data-lake/gold/breweries_aggregated/"
):
    spark = create_spark_session("GoldLayerAggregator")
    pipeline = GoldLayerAggregator(spark, input_path, output_path)
    pipeline.run_pipeline()

def failure_hook(flow, flow_run, state):
    exception = state.result(raise_on_failure=False)
    msg = f"❌ Flow '{flow.name}' failed with error: {exception}"
    send_webhook_notification.fn(msg)

@flow(name="Brewery ETL", on_failure=[failure_hook])
def brewery_etl_pipeline():
    run_brewery_data_pipeline()
    run_silver_layer_processor()
    run_gold_aggregator()


if __name__ == "__main__":
    brewery_etl_pipeline()
