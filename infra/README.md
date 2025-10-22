# Azure Deployment

This folder contains a Bicep template for provisioning the Azure resources needed to run the Streamlit-based Power & Gas Trader Shift Handover application.

## Prerequisites
- Azure subscription and permissions to deploy resources.
- Azure CLI (`az`) version 2.50.0 or later.
- Logged in with `az login` and targeting the desired subscription.

## Parameters
| Name | Description | Default |
| --- | --- | --- |
| `location` | Azure region for all resources. Defaults to the resource group location. | `resourceGroup().location` |
| `appName` | Globally unique name for the App Service. | n/a |
| `appServicePlanSku` | App Service plan SKU (`F1`, `B1`, `B2`, `B3`, `S1`, `P1v2`, `P2v2`, `P3v2`). | `B1` |
| `pythonVersion` | Python runtime to configure (`PYTHON|3.10` or `PYTHON|3.11`). | `PYTHON|3.11` |
| `appPort` | Port exposed by the Streamlit server. | `8501` |

## Deployment
1. Create or select a resource group:
   ```powershell
   az group create --name shift-handover-rg --location westeurope
   ```
2. Deploy the infrastructure:
   ```powershell
   az deployment group create `
     --resource-group shift-handover-rg `
     --template-file infra/main.bicep `
     --parameters appName=hondo-handover-app
   ```

The deployment outputs include the default host name of the web app plus the storage account and file share names used for persistent SQLite data.

## Code Deployment
After the infrastructure is in place, deploy application code to the web app. A simple option is to push a ZIP package built from this repository:
```powershell
$zipPath = "shift-handover.zip"
Compress-Archive -Path * -DestinationPath $zipPath -Force
az webapp deploy `
  --resource-group shift-handover-rg `
  --name hondo-handover-app `
  --src-path $zipPath
```

Once the deployment finishes, browse to the URL returned in the deployment output to verify the Streamlit application is running.
