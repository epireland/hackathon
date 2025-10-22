# Azure Container Registry (ACR) Deployment Guide

This guide explains how to build and deploy the Shift Handover application using Azure Container Registry and Azure Container Instances or Azure App Service.

## Prerequisites

- Azure CLI installed ([Install Guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
- Azure subscription
- Docker Desktop (for local builds)
- Contributor access to Azure subscription

## Quick Start

### Option 1: Using Build Scripts (Recommended)

#### Windows:
```cmd
azure-acr-build.bat
```

#### Linux/Mac:
```bash
chmod +x azure-acr-build.sh
./azure-acr-build.sh
```

The script will:
1. Check Azure CLI login status
2. Verify or create Azure Container Registry
3. Login to ACR
4. Let you choose between local or remote build
5. Build and push the Docker image

### Option 2: Manual Commands

See detailed commands below.

## Azure Container Registry Setup

### 1. Create Resource Group (if needed)

```bash
# Set variables
RESOURCE_GROUP="rg-shift-handover"
LOCATION="eastus"
ACR_NAME="acrshifthandover"  # Must be globally unique, lowercase, alphanumeric

# Create resource group
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION
```

### 2. Create Azure Container Registry

```bash
# Create ACR with Basic SKU
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic

# Or use Standard/Premium for production
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Standard
```

### 3. Login to ACR

```bash
az acr login --name $ACR_NAME
```

## Build Options

### Option A: Remote Build using ACR Tasks (Recommended)

ACR Tasks builds your image in Azure, so you don't need Docker installed locally.

```bash
# Build using ACR Tasks
az acr build \
  --registry $ACR_NAME \
  --image shift-handover:latest \
  --file Dockerfile \
  .

# With custom tag
az acr build \
  --registry $ACR_NAME \
  --image shift-handover:v1.0.0 \
  --file Dockerfile \
  .
```

**Benefits:**
- ✅ No local Docker required
- ✅ Faster uploads (only source code, not layers)
- ✅ Build logs stored in Azure
- ✅ Integrated with Azure security
- ✅ Can use build arguments

**Advanced ACR Build with Build Args:**
```bash
az acr build \
  --registry $ACR_NAME \
  --image shift-handover:latest \
  --file Dockerfile \
  --build-arg DB_PATH=/app/data/shift_handover.db \
  .
```

### Option B: Local Build and Push

Build locally and push to ACR.

```bash
# Get ACR login server
ACR_LOGIN_SERVER="${ACR_NAME}.azurecr.io"

# Build image
docker build -t ${ACR_LOGIN_SERVER}/shift-handover:latest .

# Push to ACR
docker push ${ACR_LOGIN_SERVER}/shift-handover:latest
```

## Managing Images in ACR

### List Repositories

```bash
az acr repository list \
  --name $ACR_NAME \
  --output table
```

### List Tags for an Image

```bash
az acr repository show-tags \
  --name $ACR_NAME \
  --repository shift-handover \
  --output table
```

### Show Image Manifest

```bash
az acr repository show \
  --name $ACR_NAME \
  --repository shift-handover \
  --output json
```

### Delete an Image Tag

```bash
az acr repository delete \
  --name $ACR_NAME \
  --image shift-handover:v1.0.0 \
  --yes
```

## Deployment Options

### Option 1: Azure Container Instances (ACI)

Simplest way to run a container in Azure.

```bash
# Create container instance
az container create \
  --resource-group $RESOURCE_GROUP \
  --name shift-handover-aci \
  --image ${ACR_NAME}.azurecr.io/shift-handover:latest \
  --registry-login-server ${ACR_NAME}.azurecr.io \
  --registry-username $(az acr credential show --name $ACR_NAME --query username -o tsv) \
  --registry-password $(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv) \
  --dns-name-label shift-handover-app \
  --ports 8501 \
  --cpu 1 \
  --memory 1.5 \
  --environment-variables DB_PATH=/app/data/shift_handover.db \
  --azure-file-volume-account-name <storage-account> \
  --azure-file-volume-account-key <storage-key> \
  --azure-file-volume-share-name shift-handover-data \
  --azure-file-volume-mount-path /app/data

# Get container public IP
az container show \
  --resource-group $RESOURCE_GROUP \
  --name shift-handover-aci \
  --query ipAddress.fqdn \
  --output tsv
```

Access at: `http://<fqdn>:8501`

### Option 2: Azure App Service (Web App for Containers)

More features for production workloads.

```bash
# Create App Service Plan
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
  --deployment-container-image-name ${ACR_NAME}.azurecr.io/shift-handover:latest

# Configure ACR credentials
az webapp config container set \
  --name shift-handover-webapp \
  --resource-group $RESOURCE_GROUP \
  --docker-custom-image-name ${ACR_NAME}.azurecr.io/shift-handover:latest \
  --docker-registry-server-url https://${ACR_NAME}.azurecr.io \
  --docker-registry-server-user $(az acr credential show --name $ACR_NAME --query username -o tsv) \
  --docker-registry-server-password $(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)

# Configure app settings
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name shift-handover-webapp \
  --settings WEBSITES_PORT=8501 DB_PATH=/home/data/shift_handover.db

# Enable continuous deployment (optional)
az webapp deployment container config \
  --name shift-handover-webapp \
  --resource-group $RESOURCE_GROUP \
  --enable-cd true

# Get webhook URL for CI/CD
az webapp deployment container show-cd-url \
  --name shift-handover-webapp \
  --resource-group $RESOURCE_GROUP
```

Access at: `https://shift-handover-webapp.azurewebsites.net`

### Option 3: Azure Kubernetes Service (AKS)

For scalable, production-grade deployments.

```bash
# Create AKS cluster
az aks create \
  --resource-group $RESOURCE_GROUP \
  --name aks-shift-handover \
  --node-count 2 \
  --attach-acr $ACR_NAME \
  --generate-ssh-keys

# Get credentials
az aks get-credentials \
  --resource-group $RESOURCE_GROUP \
  --name aks-shift-handover

# Deploy using kubectl
kubectl apply -f kubernetes/deployment.yaml
```

## Environment Variables

Set these environment variables when deploying:

- `DB_PATH`: Path to SQLite database (default: `/app/data/shift_handover.db`)
- `STREAMLIT_SERVER_PORT`: Port for Streamlit (default: `8501`)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: `0.0.0.0`)

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Deploy to ACR

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Build and Push to ACR
      run: |
        az acr build \
          --registry ${{ secrets.ACR_NAME }} \
          --image shift-handover:${{ github.sha }} \
          --image shift-handover:latest \
          --file Dockerfile \
          .
```

### Azure DevOps Pipeline Example

```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

variables:
  acrName: 'acrshifthandover'
  imageName: 'shift-handover'

steps:
- task: AzureCLI@2
  displayName: 'Build and Push to ACR'
  inputs:
    azureSubscription: 'Azure-Connection'
    scriptType: 'bash'
    scriptLocation: 'inlineScript'
    inlineScript: |
      az acr build \
        --registry $(acrName) \
        --image $(imageName):$(Build.BuildId) \
        --image $(imageName):latest \
        --file Dockerfile \
        .
```

## Security Best Practices

### 1. Use Managed Identity (Recommended)

Instead of admin credentials:

```bash
# Enable system-assigned managed identity for Web App
az webapp identity assign \
  --resource-group $RESOURCE_GROUP \
  --name shift-handover-webapp

# Get the principal ID
PRINCIPAL_ID=$(az webapp identity show \
  --resource-group $RESOURCE_GROUP \
  --name shift-handover-webapp \
  --query principalId \
  --output tsv)

# Grant AcrPull permission
az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role AcrPull \
  --scope $(az acr show --name $ACR_NAME --query id --output tsv)
```

### 2. Disable Admin User

```bash
az acr update \
  --name $ACR_NAME \
  --admin-enabled false
```

### 3. Use Private Endpoints

```bash
# For production, use private endpoints
az acr update \
  --name $ACR_NAME \
  --public-network-enabled false
```

### 4. Enable Defender for Cloud

```bash
az security pricing create \
  --name ContainerRegistry \
  --tier Standard
```

## Monitoring and Logging

### Enable Diagnostic Logs

```bash
# Create Log Analytics workspace
az monitor log-analytics workspace create \
  --resource-group $RESOURCE_GROUP \
  --workspace-name law-shift-handover

# Get workspace ID
WORKSPACE_ID=$(az monitor log-analytics workspace show \
  --resource-group $RESOURCE_GROUP \
  --workspace-name law-shift-handover \
  --query id \
  --output tsv)

# Enable diagnostics for ACR
az monitor diagnostic-settings create \
  --name acr-diagnostics \
  --resource $(az acr show --name $ACR_NAME --query id --output tsv) \
  --workspace $WORKSPACE_ID \
  --logs '[{"category": "ContainerRegistryRepositoryEvents", "enabled": true}]'
```

### View Logs

```bash
# ACR build logs
az acr task logs \
  --registry $ACR_NAME

# Container instance logs
az container logs \
  --resource-group $RESOURCE_GROUP \
  --name shift-handover-aci

# Web App logs
az webapp log tail \
  --resource-group $RESOURCE_GROUP \
  --name shift-handover-webapp
```

## Cost Optimization

- Use **Basic SKU** for development/testing
- Use **Standard SKU** for production
- Use **Premium SKU** for geo-replication and advanced features
- Consider **Reserved Instances** for ACI/App Service
- Clean up old images regularly

## Troubleshooting

### Cannot pull image from ACR

```bash
# Check ACR credentials
az acr credential show --name $ACR_NAME

# Test login
az acr login --name $ACR_NAME

# Verify image exists
az acr repository show --name $ACR_NAME --repository shift-handover
```

### Build fails with uv installation

If the build fails during uv installation, check internet connectivity from the build environment.

### Container fails to start

```bash
# Check container logs
az container logs --resource-group $RESOURCE_GROUP --name shift-handover-aci

# Check events
az container show --resource-group $RESOURCE_GROUP --name shift-handover-aci --query instanceView
```

## Quick Reference Commands

```bash
# Build remotely
az acr build --registry $ACR_NAME --image shift-handover:latest --file Dockerfile .

# List images
az acr repository list --name $ACR_NAME --output table

# List tags
az acr repository show-tags --name $ACR_NAME --repository shift-handover --output table

# Pull image
docker pull ${ACR_NAME}.azurecr.io/shift-handover:latest

# Run locally from ACR
docker run -d -p 8501:8501 ${ACR_NAME}.azurecr.io/shift-handover:latest
```

## Support

For Azure-specific issues:
- [Azure Container Registry Documentation](https://docs.microsoft.com/azure/container-registry/)
- [Azure Container Instances Documentation](https://docs.microsoft.com/azure/container-instances/)
- [Azure App Service Documentation](https://docs.microsoft.com/azure/app-service/)

---

**Ready to deploy to Azure!** ☁️🚀
