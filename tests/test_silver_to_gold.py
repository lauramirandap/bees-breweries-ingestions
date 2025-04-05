from tests.spark_test_base import SparkTestBase
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jobs.silver_to_gold import GoldLayerAggregator  

class TestGoldLayerAggregator(SparkTestBase):
    def test_aggregate_data(self):
        data = [
            {"state": "CA", "city": "San Diego", "brewery_type": "micro"},
            {"state": "CA", "city": "San Diego", "brewery_type": "micro"},
            {"state": "CA", "city": "Los Angeles", "brewery_type": "brewpub"},
            {"state": "NY", "city": "New York", "brewery_type": "micro"},
        ]
        df = self.spark.createDataFrame(data)

        aggregator = GoldLayerAggregator(self.spark, "fake/input", "fake/output")
        result_df = aggregator.aggregate_data(df)

        expected_data = [
            {"state": "CA", "city": "San Diego", "brewery_type": "micro", "brewery_count": 2},
            {"state": "CA", "city": "Los Angeles", "brewery_type": "brewpub", "brewery_count": 1},
            {"state": "NY", "city": "New York", "brewery_type": "micro", "brewery_count": 1},
        ]
        expected_df = self.spark.createDataFrame(expected_data)

        self.assertEqual(
            sorted([row.asDict() for row in result_df.collect()], key=lambda x: (x["state"], x["city"], x["brewery_type"])),
            sorted([row.asDict() for row in expected_df.collect()], key=lambda x: (x["state"], x["city"], x["brewery_type"]))
        )
