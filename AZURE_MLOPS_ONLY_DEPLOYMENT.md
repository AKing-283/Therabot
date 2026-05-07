# Azure MLOps-Only Deployment Guide (No Gemini)

This guide deploys only the emotion-model + MLflow workflow.

## 1) Local Build Test

```powershell
docker build -t therabot-mlops:local .
docker run --rm -p 8000:8000 `
  -e PORT=8000 `
  -e MLFLOW_TRACKING_URI=http://host.docker.internal:5000 `
  -e MODEL_NAME=TherabotEmotionModel `
  -e MODEL_STAGE=Production `
  therabot-mlops:local
```

Health check:

```powershell
curl http://127.0.0.1:8000/health
```

## 2) Azure Resources (CLI)

```powershell
az login
az account set --subscription "<SUBSCRIPTION_ID>"

$RG="rg-therabot-mlops"
$LOC="eastus"
$ACR="therabotmlopsacr"
$PLAN="plan-therabot-mlops"
$APP="app-therabot-mlops"

az group create --name $RG --location $LOC
az acr create --resource-group $RG --name $ACR --sku Basic
az appservice plan create --name $PLAN --resource-group $RG --is-linux --sku B1
az webapp create --resource-group $RG --plan $PLAN --name $APP --deployment-container-image-name "mcr.microsoft.com/appsvc/staticsite:latest"
```

## 3) Build and Push Image to ACR

```powershell
az acr build --registry $ACR --image therabot-mlops:latest .
```

## 4) Configure App Service Container

```powershell
$ACR_LOGIN_SERVER=$(az acr show --name $ACR --query loginServer -o tsv)
az webapp config container set `
  --name $APP `
  --resource-group $RG `
  --container-image-name "$ACR_LOGIN_SERVER/therabot-mlops:latest"
```

Enable managed identity and grant `AcrPull`:

```powershell
az webapp identity assign --name $APP --resource-group $RG
$PRINCIPAL_ID=$(az webapp identity show --name $APP --resource-group $RG --query principalId -o tsv)
$ACR_ID=$(az acr show --name $ACR --resource-group $RG --query id -o tsv)
az role assignment create --assignee $PRINCIPAL_ID --scope $ACR_ID --role AcrPull
```

## 5) App Settings

```powershell
az webapp config appsettings set `
  --name $APP `
  --resource-group $RG `
  --settings `
    PORT=8000 `
    MLFLOW_TRACKING_URI="<YOUR_MLFLOW_URI>" `
    MODEL_NAME="TherabotEmotionModel" `
    MODEL_STAGE="Production" `
    WEBSITES_PORT=8000
```

## 6) Verify Deployment

```powershell
$URL="https://$APP.azurewebsites.net"
curl "$URL/health"
curl "$URL/metrics"
```

## Notes

- This app expects MLflow tracking URI reachable from Azure App Service.
- For production DB, replace SQLite with Azure Database for PostgreSQL.
- Keep retraining as a separate scheduled job/pipeline, not in web request path.

## GitHub Actions Secrets (if using `.github/workflows/mlops-appservice.yml`)

- `AZURE_CREDENTIALS` (service principal JSON from `az ad sp create-for-rbac`)
- `ACR_LOGIN_SERVER` (example: `myregistry.azurecr.io`)
- `ACR_USERNAME`
- `ACR_PASSWORD`
- `AZURE_WEBAPP_NAME`
