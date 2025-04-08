import requests
import json
import time
import io
import os
from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv
from pathlib import Path
from jobs.utils import logger


class BreweryDataPipeline:
    def __init__(self, bucket_name, prefix="bronze/breweries/", page_size=200, max_retries=2):

        env_path = Path(__file__).resolve().parent.parent / ".env"
        load_dotenv(dotenv_path=env_path)

        self.api_url = os.getenv("BREWERY_API_URL")
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.page_size = page_size
        self.max_retries = max_retries
        self.s3_client = Minio(
            os.getenv("MINIO_ENDPOINT"),
            access_key=os.getenv("MINIO_ACCESS_KEY"),
            secret_key=os.getenv("MINIO_SECRET_KEY"),
            secure=False
        )
    
    def create_beer_data_lake_bucket(self):

        bucket_name = "beer-data-lake"

        try:
            if not self.s3_client.bucket_exists(bucket_name):
                self.s3_client.make_bucket(bucket_name)
                logger.info(f"✅ Bucket '{bucket_name}' successfully created.")
            else:
                logger.info(f"ℹ️ Bucket '{bucket_name}' already exists.")
        except S3Error as e:
            logger.info(f"❌ Error creating bucket '{bucket_name}': {e}")

    def fetch_page(self, page):
        params = {"per_page": self.page_size, "page": page}
        retries = 0

        while retries < self.max_retries:
            try:
                response = requests.get(self.api_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    return response.json()

                logger.info(f"[{response.status_code}] Error fetching page {page}, attempt {retries + 1}")
                
            except requests.exceptions.RequestException as e:
                logger.info(f"Request error: {e}, attempt {retries + 1}")
            
            retries += 1
            time.sleep(2 ** retries)

        logger.info(f"Failed to fetch page {page} after {self.max_retries} attempts.")
        return None

    def save_to_minio(self, data, page):

        if not data:
            logger.info(f"No data to save for page {page}.")
            return

        file_key = f"{self.prefix}breweries_page_{page}.json"
        ndjson_data = "\n".join(json.dumps(item) for item in data).encode("utf-8")

        try:
            self.s3_client.put_object(
                bucket_name=self.bucket_name,
                object_name=file_key,
                data=io.BytesIO(ndjson_data),
                length=len(ndjson_data),
                content_type="application/json"
            )
            logger.info(f"Page {page} saved to bucket '{self.bucket_name}' as '{file_key}'.")

        except S3Error as e:
            logger.info(f"Error saving page {page}: {e}")

    def run_pipeline(self, max_pages=50):
        for page in range(1, max_pages + 1):
            logger.info(f"Processing page {page}...")
            data = self.fetch_page(page)
            self.save_to_minio(data, page)
