from tests.spark_test_base import SparkTestBase
from pyspark.sql import Row
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jobs.bronze_to_silver import SilverLayerProcessor  


class TestSilverLayerProcessor(SparkTestBase):
    def test_transform_data_filters_nulls(self):
        input_data = [
            Row(id=1, name="Brewery A", state="CA", city="San Diego"),
            Row(id=2, name="Brewery B", state=None, city="Los Angeles"),
            Row(id=3, name="Brewery C", state="NY", city=None),
            Row(id=4, name="Brewery D", state="TX", city="Austin")
        ]

        input_df = self.spark.createDataFrame(input_data)
        processor = SilverLayerProcessor(self.spark, "", "")
        result_df = processor.transform_data(input_df)

        result = result_df.select("name").toPandas()["name"].tolist()
        expected = ["Brewery A", "Brewery D"]

        self.assertListEqual(result, expected)
