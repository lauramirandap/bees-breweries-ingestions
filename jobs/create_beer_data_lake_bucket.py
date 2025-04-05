from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv
from pathlib import Path
import os

def create_beer_data_lake_bucket():
    # Carrega variáveis do .env
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)

    # Lê variáveis de ambiente
    minio_endpoint = os.getenv("MINIO_ENDPOINT")
    minio_access_key = os.getenv("MINIO_ACCESS_KEY")
    minio_secret_key = os.getenv("MINIO_SECRET_KEY")
    bucket_name = os.getenv("MINIO_BUCKET_NAME")

    # Cria o cliente do MinIO
    client = Minio(
        minio_endpoint,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=False  # MinIO local geralmente não usa HTTPS
    )

    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"✅ Bucket '{bucket_name}' criado com sucesso.")
        else:
            print(f"ℹ️ Bucket '{bucket_name}' já existe.")
    except S3Error as e:
        print(f"❌ Erro ao criar o bucket '{bucket_name}': {e}")

if __name__ == "__main__":
    create_beer_data_lake_bucket()
