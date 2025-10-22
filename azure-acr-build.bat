@echo off
REM Azure Container Registry Build Script for Windows
REM This script builds and pushes the Docker image to Azure Container Registry

setlocal enabledelayedexpansion

echo ========================================
echo Azure Container Registry Build Script
echo ========================================
echo.

REM Configuration
set IMAGE_NAME=shift-handover
if "%IMAGE_TAG%"=="" set IMAGE_TAG=latest

REM Get ACR Name
if "%ACR_NAME%"=="" (
    set /p ACR_NAME="Enter your Azure Container Registry name: "
)

if "%ACR_NAME%"=="" (
    echo Error: ACR_NAME is required!
    exit /b 1
)

REM Get Resource Group (optional)
if "%RESOURCE_GROUP%"=="" (
    set /p RESOURCE_GROUP="Enter your Azure Resource Group name (press Enter to skip): "
)

set ACR_LOGIN_SERVER=%ACR_NAME%.azurecr.io
set FULL_IMAGE_NAME=%ACR_LOGIN_SERVER%/%IMAGE_NAME%:%IMAGE_TAG%

echo.
echo Configuration:
echo   ACR Name: %ACR_NAME%
echo   Image Name: %IMAGE_NAME%
echo   Image Tag: %IMAGE_TAG%
echo   Full Image: %FULL_IMAGE_NAME%
if not "%RESOURCE_GROUP%"=="" echo   Resource Group: %RESOURCE_GROUP%
echo.

REM Check if Azure CLI is installed
where az >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Azure CLI is not installed!
    echo Please install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
    exit /b 1
)

echo Step 1: Checking Azure CLI login status...
az account show >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Not logged in to Azure. Initiating login...
    az login
    if %ERRORLEVEL% neq 0 (
        echo Failed to login to Azure
        exit /b 1
    )
) else (
    for /f "tokens=*" %%a in ('az account show --query name -o tsv') do set ACCOUNT=%%a
    echo Already logged in to Azure: !ACCOUNT!
)
echo.

REM Check if ACR exists
echo Step 2: Verifying Azure Container Registry...
az acr show --name %ACR_NAME% >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: ACR '%ACR_NAME%' not found!
    
    if not "%RESOURCE_GROUP%"=="" (
        set /p CREATE_ACR="Would you like to create it? (y/n): "
        if /i "!CREATE_ACR!"=="y" (
            echo Creating ACR '%ACR_NAME%' in resource group '%RESOURCE_GROUP%'...
            az acr create --resource-group %RESOURCE_GROUP% --name %ACR_NAME% --sku Basic
            if %ERRORLEVEL% neq 0 (
                echo Failed to create ACR
                exit /b 1
            )
            echo ACR created successfully!
        ) else (
            exit /b 1
        )
    ) else (
        echo Please provide RESOURCE_GROUP to create the ACR or verify the ACR name.
        exit /b 1
    )
) else (
    echo ACR '%ACR_NAME%' found
)
echo.

REM Login to ACR
echo Step 3: Logging in to Azure Container Registry...
az acr login --name %ACR_NAME%
if %ERRORLEVEL% neq 0 (
    echo Failed to login to ACR
    exit /b 1
)
echo Logged in to ACR
echo.

REM Build choice
echo Step 4: Choose build method:
echo   1) Local build and push
echo   2) Remote build using ACR Tasks (recommended)
echo.
set /p BUILD_CHOICE="Enter choice (1 or 2): "

if "%BUILD_CHOICE%"=="2" (
    REM Remote build using ACR Tasks
    echo Starting remote build using ACR Tasks...
    echo This will upload the build context and build in Azure
    echo.
    
    az acr build --registry %ACR_NAME% --image %IMAGE_NAME%:%IMAGE_TAG% --file Dockerfile .
    
    if %ERRORLEVEL% neq 0 (
        echo Remote build failed!
        exit /b 1
    )
    
    echo.
    echo Remote build completed successfully!
) else (
    REM Local build and push
    echo Building Docker image locally...
    docker build -t %FULL_IMAGE_NAME% .
    
    if %ERRORLEVEL% neq 0 (
        echo Docker build failed!
        exit /b 1
    )
    echo Image built successfully
    echo.
    
    echo Pushing image to ACR...
    docker push %FULL_IMAGE_NAME%
    
    if %ERRORLEVEL% neq 0 (
        echo Docker push failed!
        exit /b 1
    )
    echo Image pushed successfully
)

echo.
echo ========================================
echo Build and Push Completed Successfully!
echo ========================================
echo.
echo Image Details:
echo   Registry: %ACR_LOGIN_SERVER%
echo   Image: %IMAGE_NAME%:%IMAGE_TAG%
echo   Full Path: %FULL_IMAGE_NAME%
echo.
echo To pull this image:
echo   docker pull %FULL_IMAGE_NAME%
echo.
echo To run this image:
echo   docker run -d -p 8501:8501 -v shift-handover-data:/app/data %FULL_IMAGE_NAME%
echo.
echo To list all images in ACR:
echo   az acr repository list --name %ACR_NAME% --output table
echo.
echo To see all tags for this image:
echo   az acr repository show-tags --name %ACR_NAME% --repository %IMAGE_NAME% --output table
echo.

endlocal
