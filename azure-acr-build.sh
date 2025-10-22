#!/bin/bash
# Azure Container Registry Build Script
# This script builds and pushes the Docker image to Azure Container Registry

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ACR_NAME="${ACR_NAME:-}"
IMAGE_NAME="shift-handover"
IMAGE_TAG="${IMAGE_TAG:-latest}"
RESOURCE_GROUP="${RESOURCE_GROUP:-}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Azure Container Registry Build Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if ACR_NAME is provided
if [ -z "$ACR_NAME" ]; then
    echo -e "${YELLOW}Enter your Azure Container Registry name:${NC}"
    read -r ACR_NAME
fi

# Check if RESOURCE_GROUP is provided
if [ -z "$RESOURCE_GROUP" ]; then
    echo -e "${YELLOW}Enter your Azure Resource Group name (press Enter to skip):${NC}"
    read -r RESOURCE_GROUP
fi

# Validate ACR_NAME
if [ -z "$ACR_NAME" ]; then
    echo -e "${RED}Error: ACR_NAME is required!${NC}"
    exit 1
fi

ACR_LOGIN_SERVER="${ACR_NAME}.azurecr.io"
FULL_IMAGE_NAME="${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${IMAGE_TAG}"

echo -e "${BLUE}Configuration:${NC}"
echo -e "  ACR Name: ${GREEN}${ACR_NAME}${NC}"
echo -e "  Image Name: ${GREEN}${IMAGE_NAME}${NC}"
echo -e "  Image Tag: ${GREEN}${IMAGE_TAG}${NC}"
echo -e "  Full Image: ${GREEN}${FULL_IMAGE_NAME}${NC}"
if [ -n "$RESOURCE_GROUP" ]; then
    echo -e "  Resource Group: ${GREEN}${RESOURCE_GROUP}${NC}"
fi
echo ""

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}Error: Azure CLI is not installed!${NC}"
    echo -e "${YELLOW}Please install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli${NC}"
    exit 1
fi

echo -e "${BLUE}Step 1: Checking Azure CLI login status...${NC}"
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}Not logged in to Azure. Initiating login...${NC}"
    az login
else
    ACCOUNT=$(az account show --query name -o tsv)
    echo -e "${GREEN}✓ Already logged in to Azure: ${ACCOUNT}${NC}"
fi
echo ""

# Check if ACR exists
echo -e "${BLUE}Step 2: Verifying Azure Container Registry...${NC}"
if ! az acr show --name "$ACR_NAME" &> /dev/null; then
    echo -e "${RED}Error: ACR '${ACR_NAME}' not found!${NC}"
    
    if [ -n "$RESOURCE_GROUP" ]; then
        echo -e "${YELLOW}Would you like to create it? (y/n)${NC}"
        read -r CREATE_ACR
        if [ "$CREATE_ACR" = "y" ]; then
            echo -e "${BLUE}Creating ACR '${ACR_NAME}' in resource group '${RESOURCE_GROUP}'...${NC}"
            az acr create --resource-group "$RESOURCE_GROUP" --name "$ACR_NAME" --sku Basic
            echo -e "${GREEN}✓ ACR created successfully!${NC}"
        else
            exit 1
        fi
    else
        echo -e "${YELLOW}Please provide RESOURCE_GROUP to create the ACR or verify the ACR name.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ ACR '${ACR_NAME}' found${NC}"
fi
echo ""

# Login to ACR
echo -e "${BLUE}Step 3: Logging in to Azure Container Registry...${NC}"
az acr login --name "$ACR_NAME"
echo -e "${GREEN}✓ Logged in to ACR${NC}"
echo ""

# Build choice
echo -e "${BLUE}Step 4: Choose build method:${NC}"
echo -e "  ${YELLOW}1)${NC} Local build and push"
echo -e "  ${YELLOW}2)${NC} Remote build using ACR Tasks (recommended)"
echo ""
read -p "Enter choice (1 or 2): " BUILD_CHOICE

if [ "$BUILD_CHOICE" = "2" ]; then
    # Remote build using ACR Tasks
    echo -e "${BLUE}Starting remote build using ACR Tasks...${NC}"
    echo -e "${YELLOW}This will upload the build context and build in Azure${NC}"
    echo ""
    
    az acr build \
        --registry "$ACR_NAME" \
        --image "${IMAGE_NAME}:${IMAGE_TAG}" \
        --file Dockerfile \
        .
    
    echo ""
    echo -e "${GREEN}✓ Remote build completed successfully!${NC}"
else
    # Local build and push
    echo -e "${BLUE}Building Docker image locally...${NC}"
    docker build -t "$FULL_IMAGE_NAME" .
    echo -e "${GREEN}✓ Image built successfully${NC}"
    echo ""
    
    echo -e "${BLUE}Pushing image to ACR...${NC}"
    docker push "$FULL_IMAGE_NAME"
    echo -e "${GREEN}✓ Image pushed successfully${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Build and Push Completed Successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Image Details:${NC}"
echo -e "  Registry: ${GREEN}${ACR_LOGIN_SERVER}${NC}"
echo -e "  Image: ${GREEN}${IMAGE_NAME}:${IMAGE_TAG}${NC}"
echo -e "  Full Path: ${GREEN}${FULL_IMAGE_NAME}${NC}"
echo ""
echo -e "${BLUE}To pull this image:${NC}"
echo -e "  ${YELLOW}docker pull ${FULL_IMAGE_NAME}${NC}"
echo ""
echo -e "${BLUE}To run this image:${NC}"
echo -e "  ${YELLOW}docker run -d -p 8501:8501 -v shift-handover-data:/app/data ${FULL_IMAGE_NAME}${NC}"
echo ""
echo -e "${BLUE}To list all images in ACR:${NC}"
echo -e "  ${YELLOW}az acr repository list --name ${ACR_NAME} --output table${NC}"
echo ""
echo -e "${BLUE}To see all tags for this image:${NC}"
echo -e "  ${YELLOW}az acr repository show-tags --name ${ACR_NAME} --repository ${IMAGE_NAME} --output table${NC}"
