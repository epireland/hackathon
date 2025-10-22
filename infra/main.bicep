@description('Azure region for all resources. Defaults to the resource group location.')
param location string = resourceGroup().location

@description('Globally unique name for the App Service hosting the Streamlit app.')
@minLength(3)
@maxLength(60)
param appName string

@description('App Service plan SKU to provision.')
@allowed([
  'F1'
  'B1'
  'B2'
  'B3'
  'S1'
  'P1v2'
  'P2v2'
  'P3v2'
])
param appServicePlanSku string = 'B1'

@description('Python runtime to configure on the App Service.')
@allowed([
  'PYTHON|3.10'
  'PYTHON|3.11'
])
param pythonVersion string = 'PYTHON|3.11'

@description('Port exposed by the Streamlit server.')
param appPort int = 8501

var planName = '${appName}-plan'
var storageNameSeed = toLower(replace(appName, '-', ''))
var storageNameRaw = '${storageNameSeed}${uniqueString(resourceGroup().id, appName)}'
var storageAccountName = substring(storageNameRaw, 0, min(length(storageNameRaw), 24))
var fileShareName = 'handoverdata'
var storageApiVersion = '2023-01-01'
var mountPath = '/home/data'

var planSkuMap = {
  F1: {
    name: 'F1'
    tier: 'Free'
    capacity: 0
  }
  B1: {
    name: 'B1'
    tier: 'Basic'
    capacity: 1
  }
  B2: {
    name: 'B2'
    tier: 'Basic'
    capacity: 1
  }
  B3: {
    name: 'B3'
    tier: 'Basic'
    capacity: 1
  }
  S1: {
    name: 'S1'
    tier: 'Standard'
    capacity: 1
  }
  P1v2: {
    name: 'P1v2'
    tier: 'PremiumV2'
    capacity: 1
  }
  P2v2: {
    name: 'P2v2'
    tier: 'PremiumV2'
    capacity: 1
  }
  P3v2: {
    name: 'P3v2'
    tier: 'PremiumV2'
    capacity: 1
  }
}

var planSku = planSkuMap[appServicePlanSku]

resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

resource storageFileService 'Microsoft.Storage/storageAccounts/fileServices@2023-01-01' = {
  name: 'default'
  parent: storage
  properties: {}
}

resource storageFileShare 'Microsoft.Storage/storageAccounts/fileServices/shares@2023-01-01' = {
  name: fileShareName
  parent: storageFileService
  properties: {
    enabledProtocols: 'SMB'
    shareQuota: 50
  }
}

resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: planName
  location: location
  sku: {
    name: planSku.name
    tier: planSku.tier
    size: planSku.name
    capacity: planSku.capacity
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

var storageKey = listKeys(storage.id, storageApiVersion).keys[0].value
var storageConnectionString = 'DefaultEndpointsProtocol=https;AccountName=${storage.name};AccountKey=${storageKey};EndpointSuffix=${environment().suffixes.storage}'

resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: appName
  location: location
  kind: 'app,linux'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: pythonVersion
      alwaysOn: true
      ftpsState: 'FtpsOnly'
      appSettings: [
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: '1'
        }
        {
          name: 'WEBSITES_PORT'
          value: string(appPort)
        }
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: 'true'
        }
        {
          name: 'STARTUP_COMMAND'
          value: 'python -m streamlit run app.py --server.port ${appPort} --server.address 0.0.0.0'
        }
        {
          name: 'STORAGE_ACCOUNT_NAME'
          value: storage.name
        }
        {
          name: 'STORAGE_FILE_SHARE'
          value: fileShareName
        }
        {
          name: 'STORAGE_MOUNT_PATH'
          value: mountPath
        }
        {
          name: 'STORAGE_CONNECTION_STRING'
          value: storageConnectionString
        }
      ]
    }
  }
  dependsOn: [
    storageFileShare
    appServicePlan
  ]
}

resource webAppConfig 'Microsoft.Web/sites/config@2023-12-01' = {
  name: '${webApp.name}/web'
  properties: {
    azureStorageAccounts: {
      data: {
        type: 'AzureFiles'
        accountName: storage.name
        shareName: fileShareName
        accessKey: storageKey
        mountPath: mountPath
      }
    }
  }
  dependsOn: [
    webApp
  ]
}

output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output storageAccount string = storage.name
output fileShare string = fileShareName
