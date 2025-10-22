#!/bin/bash
# Quick Deploy to Azure - One Command Script
# This script creates everything needed and deploys the app to Azure Container Instances

set -e

echo "================================================"
echo "Quick Deploy to Azure Container Instances"
echo "================================================"
echo ""
echo "This script will:"
echo "  1. Create a resource group"
echo "  2. Create Azure Container Registry"
echo "  3. Build the Docker image remotely"
echo "  4. Deploy to Azure Container Instances"
echo ""

# Get required inputs
read -p "Enter Azure Container Registry name (lowercase, alphanumeric): " ACR_NAME
read -p "Enter Azure location (default: eastus): " LOCATION
LOCATION=${LOCATION:-eastus}

# Generate unique names
RESOURCE_GROUP="rg-shift-handover-${ACR_NAME}"
CONTAINER_NAME="shift-handover-app"
DNS_LABEL="shift-handover-${ACR_NAME}"

echo ""
echo "Configuration:"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  ACR Name: $ACR_NAME"
echo "  Location: $LOCATION"
echo "  Container Name: $CONTAINER_NAME"
echo "  DNS Label: $DNS_LABEL"
echo ""
read -p "Continue? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "Deployment cancelled"
    exit 0
fi

echo ""
echo "Step 1/4: Creating resource group..."
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION

echo ""
echo "Step 2/4: Creating Azure Container Registry..."
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic

echo ""
echo "Step 3/4: Building Docker image remotely..."
az acr build \
  --registry $ACR_NAME \
  --image shift-handover:latest \
  --file Dockerfile \
  .

echo ""
echo "Step 4/4: Deploying to Azure Container Instances..."
az container create \
  --resource-group $RESOURCE_GROUP \
  --name $CONTAINER_NAME \
  --image ${ACR_NAME}.azurecr.io/shift-handover:latest \
  --registry-username $(az acr credential show --name $ACR_NAME --query username -o tsv) \
  --registry-password $(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv) \
  --dns-name-label $DNS_LABEL \
  --ports 8501 \
  --cpu 1 \
  --memory 1.5 \
  --environment-variables DB_PATH=/app/data/shift_handover.db

echo ""
echo "================================================"
echo "Deployment Complete!"
echo "================================================"
echo ""

# Get the FQDN
FQDN=$(az container show \
  --resource-group $RESOURCE_GROUP \
  --name $CONTAINER_NAME \
  --query ipAddress.fqdn -o tsv)

echo "Your application is available at:"
echo "  http://${FQDN}:8501"
echo ""
echo "Useful commands:"
echo "  View logs:    az container logs -g $RESOURCE_GROUP -n $CONTAINER_NAME --follow"
echo "  Restart:      az container restart -g $RESOURCE_GROUP -n $CONTAINER_NAME"
echo "  Stop:         az container stop -g $RESOURCE_GROUP -n $CONTAINER_NAME"
echo "  Delete:       az container delete -g $RESOURCE_GROUP -n $CONTAINER_NAME --yes"
echo ""
echo "To delete all resources:"
echo "  az group delete -n $RESOURCE_GROUP --yes --no-wait"
echo ""
