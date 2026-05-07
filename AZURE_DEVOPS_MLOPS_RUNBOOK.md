# Therabot Azure DevOps Runbook (MLOps-Only)

This runbook deploys the Flask + MLflow MLOps app to Azure App Service (Linux) using Azure DevOps CI/CD.

## 1) Prerequisites

- Azure subscription with permission to create/update App Service.
- Azure DevOps project and access to Pipelines.
- GitHub repository connected to Azure DevOps:
  `https://github.com/AKing-283/Therabot.git`
- Azure App Service (Linux, Python 3.11).
- MLflow tracking endpoint reachable from App Service.

## 2) Service Connection

Create an Azure Resource Manager service connection in Azure DevOps:

1. Azure DevOps -> Project Settings -> Service connections -> New service connection.
2. Select `Azure Resource Manager`.
3. Use service principal (automatic or manual).
4. Grant access permission to all pipelines if desired.
5. Save the service connection name.

## 3) Pipeline Variables to Set

Set these variables in the pipeline UI:

- `azureServiceConnection`
- `webAppName`
- `resourceGroupName`
- `mlflowTrackingUri`
- `modelName` (default `TherabotEmotionModel`)
- `modelStage` (default `Production`)

## 4) Pipeline Behavior

`azure-pipelines.yml` includes:

- Build stage:
  - Install Python 3.11
  - Install `requirements-mlops.txt`
  - Run Python compile/import checks
  - Archive source as ZIP artifact
- Deploy stage:
  - Deploy ZIP to App Service Linux
  - Configure startup command (`bash startup.sh`)
  - Configure app settings (`FLASK_ENV`, `MLFLOW_TRACKING_URI`, etc.)

## 5) Startup and Runtime

- Startup script: `startup.sh`
- Gunicorn command:

```bash
gunicorn --bind=0.0.0.0:${PORT} --timeout 600 app.app:app
```

## 6) Post-Deployment Validation

Run these checks after deployment:

- `GET /health` -> should return JSON with `status: ok`
- `POST /chat` -> should return bot reply and emotion
- `POST /retrain` -> should trigger train/retrain and promotion check
- `GET /metrics` -> should show updated metrics after retrain

