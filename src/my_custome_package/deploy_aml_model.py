import os
from azureml.core.environment import Environment
from azureml.core.model import InferenceConfig, Model
from azureml.core.webservice import AciWebservice, Webservice
from my_custom_package.utils.aml_interface import AMLInterface
from my_custom_package.utils.const import (
    AML_ENV_NAME, DEPLOYMENT_SERVICE_NAME, MODEL_NAME)


__here__ = os.path.dirname(__file__)

# The script that’s run in the web service, is score.py.
def get_inference_config(aml_interface):
    aml_env = Environment.get(
        workspace=aml_interface.workspace,
        name=AML_ENV_NAME
    )
    scoring_script_path = os.path.join(__here__, 'score.py')
    inference_config = InferenceConfig(
        entry_script=scoring_script_path,
        environment=aml_env
    )
    return inference_config




# When we get the inference configuration in the get_inference_config function we define an azureml.core.model.InferenceConfig object.
# When defining the inference configuration, the scoring script path is to score.py in the same directory as the deploy_aml_model.py and the environment Azure ML environment we created in the environment pipeline.
# We then define an Azure Container Instances web service AciWebservice configuration with a minimal requirements of just a single CPU core, with 1 GB of memory.



# The LighGbm regression model that we trained and registered in the model training pipeline is then retrieved from our workspace.
# We use this model, the inference configuration, deployment configuration and workspace to deploy a web service. While deploying the web service, the output of the service deployment is logged to the console.
# At the end of the deployment, we print the URI of this scoring web service.


def deploy_service(aml_interface):
    inference_config = get_inference_config(aml_interface)
    deployment_config = AciWebservice.deploy_configuration(
        cpu_cores=1,
        memory_gb=1
    )
    model = aml_interface.workspace.models.get(MODEL_NAME)
    service = Model.deploy(
        aml_interface.workspace,
        DEPLOYMENT_SERVICE_NAME,
        [model],
        inference_config,
        deployment_config)
    service.wait_for_deployment(show_output=True)
    print(service.scoring_uri)
    
# The output of the service deployment is logged to the console.
# At the end of the deployment, we print the URI of this scoring web service.


    
# If the service does already exist, we run update_service instead:
# This will update the service with the latest model instead of creating a new service.
def update_service(aml_interface):
    inference_config = get_inference_config(aml_interface)
    service = Webservice(
        name=DEPLOYMENT_SERVICE_NAME,
        workspace=aml_interface.workspace
    )
    model = aml_interface.workspace.models.get(MODEL_NAME)
    service.update(models=[model], inference_config=inference_config)
    print(service.state)
    print(service.scoring_uri)


def main():
    # Retrieve vars from env
    workspace_name = os.environ['AML_WORKSPACE_NAME']
    resource_group = os.environ['RESOURCE_GROUP']
    subscription_id = os.environ['SUBSCRIPTION_ID']

    spn_credentials = {
        'tenant_id': os.environ['TENANT_ID'],
        'service_principal_id': os.environ['SPN_ID'],
        'service_principal_password': os.environ['SPN_PASSWORD'],
    }

    aml_interface = AMLInterface(
        spn_credentials, subscription_id, workspace_name, resource_group
    )
    webservices = aml_interface.workspace.webservices.keys()
    if DEPLOYMENT_SERVICE_NAME not in webservices:
        deploy_service(aml_interface)
    else:
        update_service(aml_interface)


if __name__ == '__main__':
    main()

