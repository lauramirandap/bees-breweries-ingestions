import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jobs.ingest_breweries_from_api import BreweryDataPipeline


class TestBreweryDataPipeline(unittest.TestCase):

    @patch("jobs.ingest_breweries_from_api.requests.get")
    @patch("jobs.ingest_breweries_from_api.Minio")
    def test_fetch_page_success(self, mock_minio, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "name": "Test Brewery"}]
        mock_get.return_value = mock_response

        pipeline = BreweryDataPipeline("beer-data-lake")
        data = pipeline.fetch_page(1)

        self.assertIsInstance(data, list)
        self.assertEqual(data[0]["name"], "Test Brewery")

    @patch("jobs.ingest_breweries_from_api.Minio")
    def test_save_to_minio(self, mock_minio_class):
        mock_minio = MagicMock()
        mock_minio_class.return_value = mock_minio
        mock_minio.bucket_exists.return_value = True

        pipeline = BreweryDataPipeline("beer-data-lake")
        data = [{"id": 1, "name": "Test Brewery"}]

        pipeline.save_to_minio(data, 1)

        mock_minio.put_object.assert_called_once()
        args, kwargs = mock_minio.put_object.call_args
        self.assertIn("breweries_page_1.json", kwargs["object_name"])

if __name__ == "__main__":
    unittest.main()