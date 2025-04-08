from prefect.deployments import Deployment
from orchestration.prefect.flow import brewery_etl_pipeline

if __name__ == "__main__":
    deployment = Deployment.build_from_flow(
        flow=brewery_etl_pipeline,
        name="brewery-etl-deployment",
        work_pool_name="default",
        tags=["brewery", "etl"],
        description="ETL pipeline for brewery data using MinIO and Spark",
        schedule={
            "cron": "0 8 * * *",
            "timezone": "America/Sao_Paulo"
        }
    )

    deployment.apply()