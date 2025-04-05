FROM apache/spark:3.5.0

# Troca para root para poder instalar coisas
USER root

# Instala pip e a biblioteca minio
RUN apt-get update && \
    apt-get install -y python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip3 install --no-cache-dir \
        minio \
        pyspark \
        dotenv \
        requests \
        pytest \
        pandas \
        setuptools

RUN curl -o /opt/spark/jars/hadoop-aws-3.3.1.jar https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.1/hadoop-aws-3.3.1.jar && \
    curl -o /opt/spark/jars/aws-java-sdk-bundle-1.11.1026.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.1026/aws-java-sdk-bundle-1.11.1026.jar && \
    curl -o /opt/spark/jars/delta-spark_2.12-3.0.0.jar https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.0.0/delta-spark_2.12-3.0.0.jar

# Volta para o usuário padrão do Spark (por segurança e compatibilidade)
USER 185

# Diretório de trabalho dentro do container
WORKDIR /app