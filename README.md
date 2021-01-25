# AzurePipelineForPredictionCinemaOccupancyRate


Azure Pipelines are cloud-hosted pipelines that are fully integrated with Azure DevOps. You can either use a yaml file or a UI-based tool in Azure DevOps to set up your pipelines.



This resources we will create are:
Azure DevOps
This is where we’ll store our code (Azure Repos) and deploy our pipelines (Azure Pipelines)
Azure Storage
This is where we’ll store our datasets
Azure Machine Learning
Azure ML will be used for model, environment, dataset and web service management



 Set Up Azure DevOps:
 I will import all the files from GitHub repository  to the Azure DevOps

Create Azure Resources using Azure CLI:
Create a Resource Group
az group create --name <resource-group> --location <location>
Create an Azure Machine Learning Workspace
az ml workspace create -w <workspace-name> -g <resource-group>
Create an Azure Storage Account
az storage account create --name <storage-account-name> \
    --resource-group <resource-group> \
    --location <location> \
    --sku Standard_ZRS \
    --encryption blob


Create a Service Principal with Password Authentication
az ad sp create-for-rbac --name <spn-name>
Create an Azure Key Vault
az keyvault create --name <keyvault-name> \
    --resource-group <resource-group> \
    --location <location>
Store Secrets in Azure Key Vault
az keyvault secret set --vault-name <keyvault-name> --name "StorageAccountKey" --value <storage-account-key>
az keyvault secret set --vault-name <keyvault-name> --name "SpnPassword" --value <service-principle-password>
Give service principal access to Key Vault:
az keyvault set-policy -n <keyvault-name> \
    --spn <service-principle-app-id> \
    --secret-permissions get list set delete \
    --key-permissions create decrypt delete encrypt get list unwrapKey wrapKey
Give Azure DevOps Access to Key Vault
I have to do it in Azure DevOps portal
Add Azure Environment Variables to Azure DevOps
I have to do it in Azure DevOps portal



Environment Pipeline:
The custom package, imaginatively named  src/my_custom_package and has a very minimalist setup.py file in the src directory. 
This is installed in our pipelines from our requirements.txt file.


Environment Pipeline Definition:
 This environment Azure Pipeline will be set up as a yaml file. It can be found in the root of the repository as env_pipeline.yml.

 Create and Register Environment
We use the python script in src/my_custom_package/create_aml_env.py to create and register the environment. 


Model Training Pipeline:
Just as our other pipelines so far, our Azure Pipeline will be set up as a yaml file.

This can be found in the root of the repository as train_pipeline.yml.



Model Deployment Pipeline:
The next pipeline we’ll create is a model deployment Azure Pipeline to deploy the trained models to a web service using Azure Container Instances.

Deployment can be triggered each time a change to the model is detected using the Machine Learning plug-in for Azure DevOps.

In our git repository, this can be found in the root of the repository as deploy_pipeline.yml.
