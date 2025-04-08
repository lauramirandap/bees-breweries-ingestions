import pytest
from jobs.silver_to_gold import GoldLayerAggregator

@pytest.fixture
def aggregator(spark_session):
    return GoldLayerAggregator(spark_session, "fake/input", "fake/output")

@pytest.fixture
def input_df(spark_session):
    data = [
        {"state": "CA", "city": "San Diego", "brewery_type": "micro"},
        {"state": "CA", "city": "San Diego", "brewery_type": "micro"},
        {"state": "CA", "city": "Los Angeles", "brewery_type": "brewpub"},
        {"state": "NY", "city": "New York", "brewery_type": "micro"},
    ]
    return spark_session.createDataFrame(data)

@pytest.fixture
def expected_df(spark_session):
    expected_data = [
        {"state": "CA", "city": "San Diego", "brewery_type": "micro", "brewery_count": 2},
        {"state": "CA", "city": "Los Angeles", "brewery_type": "brewpub", "brewery_count": 1},
        {"state": "NY", "city": "New York", "brewery_type": "micro", "brewery_count": 1},
    ]
    return spark_session.createDataFrame(expected_data)

def test_aggregate_data(aggregator, input_df, expected_df):
    result_df = aggregator.aggregate_data(input_df)

    result = sorted([row.asDict() for row in result_df.collect()], key=lambda x: (x["state"], x["city"], x["brewery_type"]))
    expected = sorted([row.asDict() for row in expected_df.collect()], key=lambda x: (x["state"], x["city"], x["brewery_type"]))

    assert result == expected
