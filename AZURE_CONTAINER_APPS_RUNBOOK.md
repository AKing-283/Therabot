# Therabot MLOps Deployment: Docker + Azure Container Apps

This runbook switches deployment from App Service to Azure Container Apps (ACA) using Azure DevOps.
It is designed for your MLOps-only path (no Gemini).

## 1) What changes from App Service

- Deployment target: Azure Container Apps instead of Web App.
- Delivery unit: Docker image pushed to Azure Container Registry (ACR).
- Runtime config: ACA environment variables + ingress target port.

## 2) Files used

- `Dockerfile`
- `requirements-mlops.txt`
- `azure-pipelines-aca.yml`

## 3) One-time Azure resources (Portal UI friendly)

Create these resources in `southeastasia`:

1. Resource Group: `therabot-mlops` (already done)
2. Azure Container Registry (Basic SKU is enough for learning)
3. Azure Container Apps Environment
4. Azure Container App

Notes:
- If pipeline creates ACA env/app for you, you can skip manual ACA creation.
- ACR name must be globally unique.

## 4) Azure DevOps pipeline setup (UI)

1. Azure DevOps -> Pipelines -> New pipeline.
2. Select GitHub repo.
3. Choose existing YAML and select `azure-pipelines-aca.yml`.
4. In pipeline Variables, set:
   - `azureServiceConnection`
   - `resourceGroupName=therabot-mlops`
   - `location=southeastasia`
   - `acrName=<your_acr_name>`
   - `containerAppEnvironment=<your_aca_env_name>`
   - `containerAppName=<your_container_app_name>`
   - `mlflowTrackingUri=<reachable_mlflow_uri>`
   - `modelName=TherabotEmotionModel`
   - `modelStage=Production`
   - `dbPath=/mnt/therabot-data/therabot.db`
   - `metricsPath=/mnt/therabot-data/metrics.json`

## 5) Critical: SQLite persistence on ACA

Container Apps filesystem is ephemeral by default.
If you keep SQLite + metrics in local container path, data can reset on restart/revision.

Recommended options:

- Beginner-safe: mount Azure Files to `/mnt/therabot-data` and keep `DB_PATH`/`METRICS_PATH` there.
- Better production: move to Azure Database for PostgreSQL and Blob Storage for metrics/artifacts.

## 6) Enable external access

In ACA settings:
- Ingress: External
- Target port: `8000`
- Transport: Auto/HTTP

## 7) Verify live app

After deployment, get URL:

```bash
az containerapp show \
  --name <container_app_name> \
  --resource-group therabot-mlops \
  --query properties.configuration.ingress.fqdn -o tsv
```

Then test:

- `GET https://<fqdn>/health`
- `POST https://<fqdn>/chat`
- `POST https://<fqdn>/retrain`
- `GET https://<fqdn>/metrics`

## 8) Expected first issues and fixes

- Model load error in `/health`: `MLFLOW_TRACKING_URI` is unreachable from ACA.
- Retrain fails: missing registry model/stage in MLflow.
- Data disappears: DB/metrics stored on ephemeral container filesystem.
- Deployment fails to pull image: ACR credentials/RBAC not configured.

