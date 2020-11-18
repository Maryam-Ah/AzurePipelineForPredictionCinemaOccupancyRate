import os
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.environment import Environment
from my_custom_package.utils.aml_interface import AMLInterface
from my_custom_package.utils.const import AML_ENV_NAME


def get_dist_dir():
    __here__ = os.path.dirname(__file__)
    dist_dir = os.path.join(__here__, '..', 'dist')
    return dist_dir



# we get our wheel filepath using a custom function retrieve_whl_filepath
# This file uses a relative path to find the wheel file for our custom package my_custom_package – the use of relative paths is best practice as each user will have a different absolute path to files on their own system. Once we’ve got the path to the wheel file, we can add that as a private pip wheel, which will return us a URL to our wheel.

def retrieve_whl_filepath():
    dist_dir = get_dist_dir()
    if not os.path.isdir(dist_dir):
        raise FileNotFoundError("Couldn't find dist directory")
    dist_files = os.listdir(dist_dir)
    whl_file = [
        f for f in dist_files
        if f.startswith('my_custom_package')
        and f.endswith('whl')
    ]
    if not whl_file:
        raise FileNotFoundError("Couldn't find wheel file")
    return os.path.join(dist_dir, whl_file[0])


# We  instantiate a azureml.core.conda_dependencies.CondaDependencies object, to which we can add conda and pip dependencies.
# In the next few lines, we add external pip packages we’ll need in our training/scoring environment, these include numpy and pandas for data transformation, scikit-learn for machine learning model training and evaluation and joblib for model serialisation/deserialisation. This could be done by reading from a requirements.txt file but, for simplicity’s sake in this example, we add them individually manually.

def create_aml_environment(aml_interface):
    aml_env = Environment(name=AML_ENV_NAME)
    conda_dep = CondaDependencies()
    conda_dep.add_pip_package("numpy==1.18.2")
    conda_dep.add_pip_package("pandas==1.0.3")
    conda_dep.add_pip_package("scikit-learn==0.22.2.post1")
    conda_dep.add_pip_package("joblib==0.14.1")
    Next we get our wheel filepath using a custom function retrieve_whl_filepath
    whl_filepath = retrieve_whl_filepath()
    whl_url = Environment.add_private_pip_wheel(
        workspace=aml_interface.workspace,
        file_path=whl_filepath,
        exist_ok=True
    )
    conda_dep.add_pip_package(whl_url)
    aml_env.python.conda_dependencies = conda_dep
    aml_env.docker.enabled = True
    return aml_env


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
    aml_env = create_aml_environment(aml_interface)
    aml_interface.register_aml_environment(aml_env)


if __name__ == '__main__':
    main()

