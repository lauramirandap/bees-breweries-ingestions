import pytest
from pyspark.sql import Row
from jobs.bronze_to_silver import SilverLayerProcessor

@pytest.fixture
def input_data():
    return [
        Row(id=1, name="Brewery A", state="CA", city="San Diego"),
        Row(id=2, name="Brewery B", state=None, city="Los Angeles"),
        Row(id=3, name="Brewery C", state="NY", city=None),
        Row(id=4, name="Brewery D", state="TX", city="Austin")
    ]

@pytest.fixture
def processor(spark_session):
    return SilverLayerProcessor(spark_session, "", "")

@pytest.fixture
def input_df(spark_session, input_data):
    return spark_session.createDataFrame(input_data)

def test_transform_data_filters_nulls(processor, input_df):
    result_df = processor.filter_data_by_state_and_city_not_null(input_df)
    result = result_df.select("name").toPandas()["name"].tolist()
    expected = ["Brewery A", "Brewery D"]

    assert result == expected