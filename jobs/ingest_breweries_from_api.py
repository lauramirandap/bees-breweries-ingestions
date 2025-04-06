import requests
import json
import time
import io
import os
from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv
from pathlib import Path


class BreweryDataPipeline:
    def __init__(self, bucket_name, prefix="bronze/breweries/", page_size=200, max_retries=2):
        env_path = Path(__file__).resolve().parent.parent / ".env"
        load_dotenv(dotenv_path=env_path)

        print(os.getenv("BREWERY_API_URL"))
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
                print(f"✅ Bucket '{bucket_name}' criado com sucesso.")
            else:
                print(f"ℹ️ Bucket '{bucket_name}' já existe.")
        except S3Error as e:
            print(f"❌ Erro ao criar o bucket '{bucket_name}': {e}")

    def fetch_page(self, page):
        params = {"per_page": self.page_size, "page": page}
        retries = 0

        while retries < self.max_retries:
            try:
                response = requests.get(self.api_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    return response.json()

                print(f"[{response.status_code}] Erro ao buscar página {page}, tentativa {retries + 1}")
                
            except requests.exceptions.RequestException as e:
                print(f"Erro na requisição: {e}, tentativa {retries + 1}")
            
            retries += 1
            time.sleep(2 ** retries)

        print(f"Falha ao buscar página {page} após {self.max_retries} tentativas.")
        return None

    def save_to_minio(self, data, page):

        if not data:
            print(f"No data to save for page {page}.")
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
            print(f"Page {page} salva no bucket '{self.bucket_name}' como '{file_key}'.")

        except S3Error as e:
            print(f"Erro ao salvar página {page}: {e}")

    def run_pipeline(self, max_pages=50):
        for page in range(1, max_pages + 1):
            print(f"Processing page {page}...")
            data = self.fetch_page(page)
            self.save_to_minio(data, page)
