# Azure CLI Quick Reference - Shift Handover App

## Environment Setup

```bash
# Set common variables
export RESOURCE_GROUP="rg-shift-handover"
export LOCATION="eastus"
export ACR_NAME="acrshifthandover"  # lowercase, alphanumeric only
export IMAGE_NAME="shift-handover"
export IMAGE_TAG="latest"
```

## Azure Container Registry (ACR)

### Create ACR
```bash
# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create ACR (Basic SKU)
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic

# Login to ACR
az acr login --name $ACR_NAME
```

### Remote Build (Recommended)
```bash
# Build using ACR Tasks - No Docker required!
az acr build \
  --registry $ACR_NAME \
  --image $IMAGE_NAME:$IMAGE_TAG \
  --file Dockerfile \
  .

# Build with specific tag
az acr build \
  --registry $ACR_NAME \
  --image $IMAGE_NAME:v1.0.0 \
  --file Dockerfile \
  .
```

### Local Build and Push
```bash
# Build locally
docker build -t ${ACR_NAME}.azurecr.io/$IMAGE_NAME:$IMAGE_TAG .

# Push to ACR
docker push ${ACR_NAME}.azurecr.io/$IMAGE_NAME:$IMAGE_TAG
```

### Manage Images
```bash
# List repositories
az acr repository list --name $ACR_NAME --output table

# List tags for an image
az acr repository show-tags --name $ACR_NAME --repository $IMAGE_NAME --output table

# Show image details
az acr repository show --name $ACR_NAME --repository $IMAGE_NAME

# Delete a tag
az acr repository delete --name $ACR_NAME --image $IMAGE_NAME:v1.0.0 --yes

# Delete repository
az acr repository delete --name $ACR_NAME --repository $IMAGE_NAME --yes
```

## Azure Container Instances (ACI)

### Basic Deployment
```bash
# Simple container instance
az container create \
  --resource-group $RESOURCE_GROUP \
  --name shift-handover-aci \
  --image ${ACR_NAME}.azurecr.io/$IMAGE_NAME:$IMAGE_TAG \
  --registry-username $(az acr credential show --name $ACR_NAME --query username -o tsv) \
  --registry-password $(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv) \
  --dns-name-label shift-handover-app \
  --ports 8501 \
  --cpu 1 \
  --memory 1.5
```

### With Environment Variables
```bash
az container create \
  --resource-group $RESOURCE_GROUP \
  --name shift-handover-aci \
  --image ${ACR_NAME}.azurecr.io/$IMAGE_NAME:$IMAGE_TAG \
  --registry-login-server ${ACR_NAME}.azurecr.io \
  --registry-username $(az acr credential show --name $ACR_NAME --query username -o tsv) \
  --registry-password $(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv) \
  --dns-name-label shift-handover-app \
  --ports 8501 \
  --environment-variables \
    DB_PATH=/app/data/shift_handover.db \
    STREAMLIT_SERVER_PORT=8501
```

### Manage Container Instances
```bash
# Show container details
az container show --resource-group $RESOURCE_GROUP --name shift-handover-aci

# Get public IP/FQDN
az container show \
  --resource-group $RESOURCE_GROUP \
  --name shift-handover-aci \
  --query ipAddress.fqdn -o tsv

# View logs
az container logs --resource-group $RESOURCE_GROUP --name shift-handover-aci --follow

# Restart container
az container restart --resource-group $RESOURCE_GROUP --name shift-handover-aci

# Stop container
az container stop --resource-group $RESOURCE_GROUP --name shift-handover-aci

# Delete container
az container delete --resource-group $RESOURCE_GROUP --name shift-handover-aci --yes
```

## Azure App Service (Web App for Containers)

### Create and Deploy
```bash
# Create App Service Plan (Linux)
az appservice plan create \
  --name plan-shift-handover \
  --resource-group $RESOURCE_GROUP \
  --is-linux \
  --sku B1

# Create Web App
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan plan-shift-handover \
  --name shift-handover-webapp \
  --deployment-container-image-name ${ACR_NAME}.azurecr.io/$IMAGE_NAME:$IMAGE_TAG

# Configure container settings
az webapp config container set \
  --name shift-handover-webapp \
  --resource-group $RESOURCE_GROUP \
  --docker-custom-image-name ${ACR_NAME}.azurecr.io/$IMAGE_NAME:$IMAGE_TAG \
  --docker-registry-server-url https://${ACR_NAME}.azurecr.io \
  --docker-registry-server-user $(az acr credential show --name $ACR_NAME --query username -o tsv) \
  --docker-registry-server-password $(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)

# Set app settings
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name shift-handover-webapp \
  --settings \
    WEBSITES_PORT=8501 \
    DB_PATH=/home/data/shift_handover.db
```

### Manage Web App
```bash
# Browse app
az webapp browse --resource-group $RESOURCE_GROUP --name shift-handover-webapp

# View logs (streaming)
az webapp log tail --resource-group $RESOURCE_GROUP --name shift-handover-webapp

# Restart app
az webapp restart --resource-group $RESOURCE_GROUP --name shift-handover-webapp

# Stop app
az webapp stop --resource-group $RESOURCE_GROUP --name shift-handover-webapp

# Start app
az webapp start --resource-group $RESOURCE_GROUP --name shift-handover-webapp

# Show app details
az webapp show --resource-group $RESOURCE_GROUP --name shift-handover-webapp

# Delete app
az webapp delete --resource-group $RESOURCE_GROUP --name shift-handover-webapp
```

### Enable Continuous Deployment
```bash
# Enable webhook for automatic deployment on image update
az webapp deployment container config \
  --name shift-handover-webapp \
  --resource-group $RESOURCE_GROUP \
  --enable-cd true

# Get webhook URL
az webapp deployment container show-cd-url \
  --name shift-handover-webapp \
  --resource-group $RESOURCE_GROUP
```

## Monitoring & Diagnostics

### Enable Application Insights
```bash
# Create Application Insights
az monitor app-insights component create \
  --app shift-handover-insights \
  --location $LOCATION \
  --resource-group $RESOURCE_GROUP

# Get instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app shift-handover-insights \
  --resource-group $RESOURCE_GROUP \
  --query instrumentationKey -o tsv)

# Set on Web App
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name shift-handover-webapp \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY=$INSTRUMENTATION_KEY
```

### View Logs
```bash
# ACR logs
az acr task logs --registry $ACR_NAME

# Container instance logs
az container logs --resource-group $RESOURCE_GROUP --name shift-handover-aci

# Web app logs
az webapp log tail --resource-group $RESOURCE_GROUP --name shift-handover-webapp

# Download logs
az webapp log download \
  --resource-group $RESOURCE_GROUP \
  --name shift-handover-webapp \
  --log-file logs.zip
```

## Security

### Use Managed Identity (App Service)
```bash
# Enable system-assigned managed identity
az webapp identity assign \
  --resource-group $RESOURCE_GROUP \
  --name shift-handover-webapp

# Get principal ID
PRINCIPAL_ID=$(az webapp identity show \
  --resource-group $RESOURCE_GROUP \
  --name shift-handover-webapp \
  --query principalId -o tsv)

# Grant ACR pull permission
az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role AcrPull \
  --scope $(az acr show --name $ACR_NAME --query id -o tsv)

# Remove registry credentials (now using managed identity)
az webapp config container set \
  --name shift-handover-webapp \
  --resource-group $RESOURCE_GROUP \
  --docker-custom-image-name ${ACR_NAME}.azurecr.io/$IMAGE_NAME:$IMAGE_TAG \
  --docker-registry-server-url https://${ACR_NAME}.azurecr.io
```

### Disable ACR Admin User
```bash
az acr update --name $ACR_NAME --admin-enabled false
```

## Resource Management

### List Resources
```bash
# List all resources in resource group
az resource list --resource-group $RESOURCE_GROUP --output table

# Show costs
az consumption usage list --output table
```

### Cleanup
```bash
# Delete specific resources
az container delete --resource-group $RESOURCE_GROUP --name shift-handover-aci --yes
az webapp delete --resource-group $RESOURCE_GROUP --name shift-handover-webapp --yes
az appservice plan delete --resource-group $RESOURCE_GROUP --name plan-shift-handover --yes
az acr delete --resource-group $RESOURCE_GROUP --name $ACR_NAME --yes

# Delete entire resource group (careful!)
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

## PowerShell Equivalents

```powershell
# Set variables
$RESOURCE_GROUP = "rg-shift-handover"
$LOCATION = "eastus"
$ACR_NAME = "acrshifthandover"
$IMAGE_NAME = "shift-handover"
$IMAGE_TAG = "latest"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create ACR
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic

# Remote build
az acr build `
  --registry $ACR_NAME `
  --image ${IMAGE_NAME}:${IMAGE_TAG} `
  --file Dockerfile `
  .

# Get ACR credentials
$ACR_USER = az acr credential show --name $ACR_NAME --query username -o tsv
$ACR_PASSWORD = az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv

# Create container instance
az container create `
  --resource-group $RESOURCE_GROUP `
  --name shift-handover-aci `
  --image ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG} `
  --registry-username $ACR_USER `
  --registry-password $ACR_PASSWORD `
  --dns-name-label shift-handover-app `
  --ports 8501
```

## Complete Deployment Example

```bash
#!/bin/bash
# Complete deployment script

# Variables
export RESOURCE_GROUP="rg-shift-handover"
export LOCATION="eastus"
export ACR_NAME="acrshifthandover"
export IMAGE_NAME="shift-handover"
export IMAGE_TAG="latest"

# Create resources
az group create --name $RESOURCE_GROUP --location $LOCATION
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic

# Build and push
az acr build --registry $ACR_NAME --image $IMAGE_NAME:$IMAGE_TAG --file Dockerfile .

# Deploy to ACI
az container create \
  --resource-group $RESOURCE_GROUP \
  --name shift-handover-aci \
  --image ${ACR_NAME}.azurecr.io/$IMAGE_NAME:$IMAGE_TAG \
  --registry-username $(az acr credential show --name $ACR_NAME --query username -o tsv) \
  --registry-password $(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv) \
  --dns-name-label shift-handover-app \
  --ports 8501 \
  --cpu 1 \
  --memory 1.5

# Get URL
FQDN=$(az container show \
  --resource-group $RESOURCE_GROUP \
  --name shift-handover-aci \
  --query ipAddress.fqdn -o tsv)

echo "Application available at: http://${FQDN}:8501"
```

---

**Pro Tip**: Save these commands in a script for easy reuse!
