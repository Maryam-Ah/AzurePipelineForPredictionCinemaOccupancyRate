import os
from azureml.core import Datastore, Dataset


# Get data from Azure storage
__here__ = os.path.dirname(__file__)


def get_df_from_datastore_path(datastore, datastore_path):
    datastore_path = [(datastore, datastore_path)]
    dataset = Dataset.Tabular.from_delimited_files(
        path=datastore_path
    )
    dataframe = dataset.to_pandas_dataframe()
    return dataframe

