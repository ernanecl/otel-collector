# Automated Environment Setup with Docker

This project sets up an environment with the following components, all running in Docker containers:

- **FastAPI**: A simple web API with OpenTelemetry and Prometheus instrumentation.
- **OpenTelemetry Collector**: Collects and routes telemetry data.
- **Kafka + ZooKeeper**: Message broker for telemetry data.
- **Grafana**: Visualization dashboard.
- **Mimir**: Long-term storage for metrics.

## 🧰 Prerequisites

- Docker
- Docker Compose

## 🚀 How to Run

1. Clone this repository:

   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. ***Start all services

    ```bash
    docker-compose up --build
    ```

3. Access the services:
    - FastAPI: http://localhost:8000
    - Grafana: http://localhost:3000
    - Default login: admin / admin
    - Mimir: http://localhost:9000

4. Configure Grafana:
    - Add Mimir as a Prometheus data source: http://mimir:9000
    - Import your dashboard JSON via Dashboards > Import

## 🛑 How to Stop

To stop and remove all containers:

```bash
docker-compose down
```

## 📁 Project Structure

.
├── Dockerfile
├── docker-compose.yml
├── fastapi_app.py
├── otel-collector-config.yaml
├── README.md
└── grafana/ (optional volume for persistence)