# 🍺 Ingestão de Cervejarias

## 📌 Visão Geral  
Este projeto coleta dados de cervejarias a partir da API pública: [Open Brewery DB API](https://www.openbrewerydb.org/). O pipeline de ingestão é containerizado com Docker e segue uma **arquitetura medallion** (Bronze, Silver, Gold) para organizar e estruturar o processamento dos dados.

---

## ⚙️ Orquestração  
O **Prefect** é utilizado para orquestrar todas as tarefas de ingestão e transformação, garantindo agendamento confiável, tentativas automáticas e observabilidade do fluxo.

---

## 🔧 Stack Tecnológico

| Componente        | Ferramenta                        |
|------------------|-----------------------------------|
| Data Lake        | [MinIO](https://min.io/)          |
| Processamento    | [Apache Spark](https://spark.apache.org/) |
| Orquestração     | [Prefect](https://www.prefect.io/) |
| Containerização  | [Docker](https://www.docker.com/) |
| Testes           | `pytest` para testes unitários     |

---

## 🚀 Decisões do Projeto

- **Extração de Dados**: Implementada com Python e a biblioteca `requests`.
- **Processamento de Dados**: As transformações seguem a arquitetura medallion e são realizadas com PySpark.
- **Armazenamento**: Todos os dados ingeridos são salvos em buckets no MinIO, simulando um data lake compatível com S3.
- **Modularização**: O código está organizado em módulos e classes reutilizáveis, facilitando testes e manutenção.
- **Containerização**: Todo o ambiente (Spark, MinIO, API, Prefect) é orquestrado usando Docker Compose.

---

## 🧪 Testes

- Os testes unitários foram implementados com `pytest`.
- Módulos principais, como ingestão da API e escrita dos dados, estão totalmente cobertos por testes unitários.
-






Você disse:
o codigo em ingles


O ChatGPT disse:
Claro! Aqui está o conteúdo do README.md traduzido completamente para inglês, pronto para ser usado no seu repositório:

markdown
Copiar
Editar
# 🍺 Breweries Ingestion

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

## ▶️ Como Rodar o Projeto Localmente

### 📦 Pré-requisitos  
Antes de rodar o projeto, certifique-se de ter os seguintes itens instalados:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

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

### 3. Run the ingestion flow

```bash
docker exec -it prefect-agent bash
python orchestration/prefect_flow.py
```

### 4. Check the data in MinIO

Access the MinIO UI at http://localhost:9001, log in, and navigate to the configured bucket (e.g., bronze/) to see the saved files like breweries_page_*.json

---

## 🧪 Testing

- Unit tests are implemented using `pytest`.
- Core modules, such as API ingestion and data writing, are fully covered by unit tests.
- Test coverage can be expanded in future iterations to include end-to-end and integration tests.

---

## 🔄 Future Improvements

- ✅ Implement CI/CD with GitHub Actions for testing and container builds.
- ✅ Add integration tests with Prefect and Spark pipelines.
- ✅ Monitor task execution using Prefect Cloud or Prefect Server UI.
- ✅ Implement data quality checks using **Great Expectations**.
- ✅ Add documentation using tools like **MkDocs** or a `docs/` folder with usage instructions.
