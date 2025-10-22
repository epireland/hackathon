@echo off
REM Quick Deploy to Azure - One Command Script (Windows)
REM This script creates everything needed and deploys the app to Azure Container Instances

setlocal enabledelayedexpansion

echo ================================================
echo Quick Deploy to Azure Container Instances
echo ================================================
echo.
echo This script will:
echo   1. Create a resource group
echo   2. Create Azure Container Registry
echo   3. Build the Docker image remotely
echo   4. Deploy to Azure Container Instances
echo.

REM Get required inputs
set /p ACR_NAME="Enter Azure Container Registry name (lowercase, alphanumeric): "
set /p LOCATION="Enter Azure location (default: eastus): "
if "%LOCATION%"=="" set LOCATION=eastus

REM Generate unique names
set RESOURCE_GROUP=rg-shift-handover-%ACR_NAME%
set CONTAINER_NAME=shift-handover-app
set DNS_LABEL=shift-handover-%ACR_NAME%

echo.
echo Configuration:
echo   Resource Group: %RESOURCE_GROUP%
echo   ACR Name: %ACR_NAME%
echo   Location: %LOCATION%
echo   Container Name: %CONTAINER_NAME%
echo   DNS Label: %DNS_LABEL%
echo.
set /p CONFIRM="Continue? (y/n): "

if /i not "%CONFIRM%"=="y" (
    echo Deployment cancelled
    exit /b 0
)

echo.
echo Step 1/4: Creating resource group...
az group create --name %RESOURCE_GROUP% --location %LOCATION%
if %ERRORLEVEL% neq 0 exit /b 1

echo.
echo Step 2/4: Creating Azure Container Registry...
az acr create --resource-group %RESOURCE_GROUP% --name %ACR_NAME% --sku Basic
if %ERRORLEVEL% neq 0 exit /b 1

echo.
echo Step 3/4: Building Docker image remotely...
az acr build --registry %ACR_NAME% --image shift-handover:latest --file Dockerfile .
if %ERRORLEVEL% neq 0 exit /b 1

echo.
echo Step 4/4: Deploying to Azure Container Instances...
for /f "tokens=*" %%a in ('az acr credential show --name %ACR_NAME% --query username -o tsv') do set ACR_USER=%%a
for /f "tokens=*" %%a in ('az acr credential show --name %ACR_NAME% --query passwords[0].value -o tsv') do set ACR_PASSWORD=%%a

az container create ^
  --resource-group %RESOURCE_GROUP% ^
  --name %CONTAINER_NAME% ^
  --image %ACR_NAME%.azurecr.io/shift-handover:latest ^
  --registry-username %ACR_USER% ^
  --registry-password %ACR_PASSWORD% ^
  --dns-name-label %DNS_LABEL% ^
  --ports 8501 ^
  --cpu 1 ^
  --memory 1.5 ^
  --environment-variables DB_PATH=/app/data/shift_handover.db

if %ERRORLEVEL% neq 0 exit /b 1

echo.
echo ================================================
echo Deployment Complete!
echo ================================================
echo.

REM Get the FQDN
for /f "tokens=*" %%a in ('az container show --resource-group %RESOURCE_GROUP% --name %CONTAINER_NAME% --query ipAddress.fqdn -o tsv') do set FQDN=%%a

echo Your application is available at:
echo   http://%FQDN%:8501
echo.
echo Useful commands:
echo   View logs:    az container logs -g %RESOURCE_GROUP% -n %CONTAINER_NAME% --follow
echo   Restart:      az container restart -g %RESOURCE_GROUP% -n %CONTAINER_NAME%
echo   Stop:         az container stop -g %RESOURCE_GROUP% -n %CONTAINER_NAME%
echo   Delete:       az container delete -g %RESOURCE_GROUP% -n %CONTAINER_NAME% --yes
echo.
echo To delete all resources:
echo   az group delete -n %RESOURCE_GROUP% --yes --no-wait
echo.

endlocal
