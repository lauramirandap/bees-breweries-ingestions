
# 🍺 Brewery Data Ingestion Pipelin

## 📌 Overview  
This project retrieves brewery data from the public API: [Open Brewery DB API](https://www.openbrewerydb.org/). The ingestion pipeline is containerized using Docker and follows a **medallion architecture** (Bronze, Silver, Gold) for structured data processing and organization.

---

## ⚙️ Orchestration  
**Prefect** is used to orchestrate all ingestion and transformation tasks, providing reliable scheduling, automatic retries, and flow observability.

---

## 🔧 Tech Stack

| Component         | Tool                             |
|------------------|----------------------------------|
| Data Lake         | [MinIO](https://min.io/)         |
| Processing        | [Apache Spark](https://spark.apache.org/) |
| Orchestration     | [Prefect](https://www.prefect.io/) |
| Containerization  | [Docker](https://www.docker.com/) |
| Testing           | `pytest` for unit testing         |

---

## 🚀 Project Decisions

- **Data Extraction**: Implemented using Python and the `requests` library.
- **Data Processing**: All transformations follow the medallion architecture and are performed using PySpark.
- **Storage**: All ingested data is stored in MinIO buckets, simulating an S3-compatible data lake.
- **Modularization**: The code is organized into reusable modules and classes, making testing and maintenance easier.
- **Containerization**: The entire environment (Spark, MinIO, API, Prefect) is orchestrated using Docker Compose.

---

## ▶️ How to Run the Project Locally


### 📦 Prerequisites  
Before running the project, make sure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Python 3.10+](https://www.python.org/) (for local development)

---

### 🚀 Step-by-step Guide

#### 1. Clone the repository

```bash
git clone https://github.com/lauramirandap/bees-breweries-ingestions
cd bees-breweries-ingestions
```

### 2. Build and start the containers

```bash
docker-compose up --build
```

### 3. (Optional) Run the ingestion flow manually
Use this if you just want to test the flow once, without scheduling:

```bash
docker exec -it prefect bash
python orchestration/prefect/flow.py
```

### 3. Schedule the ingestion flow with Prefect
To register and schedule the flow to run automatically according to the defined schedule in brewery_deployment.py

```bash
docker exec -it prefect bash
prefect work-pool create -t process default
python orchestration/brewery_deployment.py
```

### 4. Check the data in MinIO

Access the MinIO UI at http://localhost:9001, log in, and navigate to the configured bucket (e.g., bronze/) to see the saved files like breweries_page_*.json

---

### 🔐 Environment Variables

Before running the project, create a `.env` file at the root of the repository with the following variables:

- `MINIO_ENDPOINT`
- `MINIO_ACCESS_KEY`
- `MINIO_SECRET_KEY`
- `PREFECT_API_URL`
- `BREWERY_API_URL`

> ⚠️ These environment variables are required for the project to connect to MinIO, Prefect, and the external Brewery API.

---

## 🧪 Testing

- Unit tests are implemented using `pytest`.
- Core modules, such as API ingestion and data writing, are fully covered by unit tests.
- Test coverage can be expanded in future iterations to include end-to-end and integration tests.

---

## ✅ Monitoring and Pipeline Failure Alert

This project includes an automated email alert mechanism configured with **Zapier**, which sends a notification whenever the pipeline fails.

### 🔁 How it works

The pipeline is executed using **Prefect**, which triggers a **Zapier webhook** in case of a failure.

The Zap configured in Zapier consists of two steps:

- **Catch Hook (Webhooks by Zapier)** — Receives the call from Prefect with the error details.
- **Send Email (Gmail)** — Sends an email to the technical owner with the failure information.

---

## 🔄 Future Improvements

- ✅ Implement CI/CD with GitHub Actions for testing and container builds.
- ✅ Add integration tests with Prefect and Spark pipelines.
- ✅ Implement data quality checks using **Great Expectations**.
- ✅ Add documentation using tools like **MkDocs** or a `docs/` folder with usage instructions.
- ✅ Add data versioning using Delta Lake
