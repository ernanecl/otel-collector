# Aplicação para teste local

App usado para testar recursos para o direcionamento de métricas especificas para um determinado tópico Kafka

## 1. FastAPI - v1 (path -> /otel-collector/fastapi_v1)

Aplicação base em Python com FastAPI, OpenTelemetry, Grafana e Mimir, prontos para testes locais com Docker:

- 🐳 Dockerfile — Define a imagem da aplicação FastAPI com OpenTelemetry
- 🧩 docker-compose.yml — Orquestra a aplicação, Grafana e Mimir
- 🐍 fastapi_app.py — Código da aplicação FastAPI com métricas e tracing

---

### Como testar localmente:

1. Coloque todos os arquivos no mesmo diretório.
2. Construa e suba os containers:
    ```sh
    docker-compose up --build
    ```
3. Acesse os serviços:
    - Aplicação FastAPI: http://localhost:8000
    - Métricas Prometheus: http://localhost:8000/metrics
    - Grafana: http://localhost:3000 (login: admin / senha: admin)
    - Mimir: http://localhost:9000

---

### Configuração para o Grafana com dashboards e datasources automáticos

Arquivos de configuração para o Grafana, prontos para importar e visualizar métricas da sua aplicação FastAPI com OpenTelemetry:

- 📊 grafana-dashboard.json — Dashboard com gráficos de requisições HTTP e latência (p95 e p50)
- ⚙️ grafana-datasource.json — Datasource configurado para apontar para o Mimir

---

### ✅ Como usar:

1. Acesse o Grafana em http://localhost:3000
Login padrão: admin / admin

2. Importe o datasource:
    - Vá em ⚙️ Configuration → Data Sources → Add data source
    - Escolha Prometheus
    - Use a URL: http://mimir:9000
    - Ou importe diretamente o JSON grafana-datasource.json

3. Importe o dashboard:
    - Vá em 📁 Dashboards → Import
    - Cole o conteúdo do grafana-dashboard.json ou envie o arquivo

&nbsp;

## 2. FastAPI - v2 (path -> /otel-collector/fastapi_v2)

O conjunto completo de arquivos para testar localmente uma aplicação FastAPI com OpenTelemetry, roteando métricas via Collector com routing e transform, e visualizando no Grafana com Mimir:

### 🐍 Aplicação e infraestrutura
- fastapi_app.py — Aplicação FastAPI com métricas OTLP
- Dockerfile — Imagem da aplicação
- docker-compose.yml — Orquestração com Collector, Kafka, Grafana, Mimir e MinIO

### ⚙️ OpenTelemetry Collector
- otel-collector-config.yaml — Configuração com transform e routing processors

### 📊 Grafana
- grafana-datasource.json — Datasource apontando para Mimir
- grafana-dashboard.json — Dashboard com métricas HTTP e latência

### ✅ Como rodar:

1. Coloque todos os arquivos no mesmo diretório.
2. Execute:
```sh
docker-compose up --build
```
3. Acesse:
    - FastAPI: http://localhost:8000
    - Grafana: http://localhost:3000 (login: admin / senha: admin)

&nbsp;

## 3. Gerar métricas para testar roteamento - (path -> /otel-collector/fastapi_app.py)

Novo arquivo da aplicação FastAPI com geração de métricas OTLP que incluem o atributo k8s.namespace.name, variando entre "opb", "default" e "other":

📄 fastapi_app.py

```py

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
import random

app = FastAPI()

# Setup OpenTelemetry
resource = Resource(attributes={
    "service.name": "fastapi-service",
    "k8s.namespace.name": "default"
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True))
trace.get_tracer_provider().add_span_processor(span_processor)

# Setup metrics
metric_exporter = OTLPMetricExporter(endpoint="http://otel-collector:4317", insecure=True)
metric_reader = PeriodicExportingMetricReader(metric_exporter)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
meter = meter_provider.get_meter(__name__)

request_counter = meter.create_counter(
    name="http_requests_total",
    description="Total number of HTTP requests",
    unit="1",
)

@app.get("/")
async def root():
    with tracer.start_as_current_span("root-endpoint"):
        # Simulate varying k8s.namespace.name
        namespace_name = random.choice(["opb", "default", "other"])
        trace.get_current_span().set_attribute("k8s.namespace.name", namespace_name)
        request_counter.add(1, {"k8s.namespace.name": namespace_name})
        return {"message": f"Hello, World! Namespace: {namespace_name}"}

@app.get("/metrics")
async def metrics():
    with tracer.start_as_current_span("metrics-endpoint"):
        namespace_name = random.choice(["opb", "default", "other"])
        trace.get_current_span().set_attribute("k8s.namespace.name", namespace_name)
        request_counter.add(1, {"k8s.namespace.name": namespace_name})
        return {"message": "Metrics endpoint"}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

```

Essa variação permite testar o roteamento no OpenTelemetry Collector com base no valor do namespace, conforme configurado nos processors transform e routing.

## 4. FastAPI v3 - (path -> /otel-collector/fastapi_v3)

Nova versão do sistema sem uso de Docker Compose, com todos os arquivos e instruções para executar manualmente cada componente:

### 🐍 Aplicação FastAPI com OpenTelemetry
- fastapi_app.py — Código da aplicação com métricas e tracing OTLP
- Dockerfile — Para build e execução da aplicação via Docker

### ⚙️ OpenTelemetry Collector
- otel-collector-config.yaml — Configuração com transform e routing processors

### 📄 Instruções completas
- instructions.txt (README.md) — Passo a passo para executar manualmente:
    - FastAPI
    - OpenTelemetry Collector
    - Kafka e ZooKeeper
    - Grafana
    - Mimir

### Script Bash

O script Bash para automatizar todo o processo:

🔧 automate_process.sh

Este script executa:

FastAPI via Docker
OpenTelemetry Collector
Kafka (com ZooKeeper)
Grafana
Mimir via Docker

## 5. FastAPI v4 - (path -> /otel-collector/fastapi_v4)

Como todo o ambiente será isolado e descartável, a melhor abordagem é usar Docker Compose para orquestrar todos os serviços (FastAPI, OpenTelemetry Collector, Kafka, Grafana, Mimir etc.) dentro de containers.

1. Um docker-compose.yml que define todos os serviços.
2. Um Dockerfile para o FastAPI (você já tem, e será mantido).
3. Um volume temporário para armazenar dados, que será descartado ao parar os containers.
4. Um README.md com instruções simples de uso.

---
&nbsp;

O arquivo `docker-compose.yml` orquestra os seguintes serviços:
- FastAPI (construído a partir do seu Dockerfile)
- OpenTelemetry Collector
- Kafka (com ZooKeeper)
- Grafana
- Mimir
---
&nbsp;


## 6. 

### ✅ 1. Checklist para rodar o projeto

| Requisito | Detalhes |
| --------- | -------- |
| Docker Desktop | Deve estar instalado e rodando. Inclui o Docker Engine e o Docker Compose. |
| Python | Não é necessário para rodar os containers, mas pode ser útil para scripts auxiliares. |
| Git (opcional) | Para clonar o repositório, ou você pode baixar os arquivos manualmente. |

### 🚀 2. Como rodar

1. Abra o terminal (PowerShell ou CMD) na pasta onde estão os arquivos (Dockerfile, docker-compose.yml, etc.).
2. Execute:
    ```sh
    docker-compose up --build
    ```
3. Acesse os serviços:
    - FastAPI: http://localhost:8000
    - Grafana: http://localhost:3000
    - Mimir: http://localhost:9000

### 🛑 3. Para parar tudo

```sh
docker-compose down
```