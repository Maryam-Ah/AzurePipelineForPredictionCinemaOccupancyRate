import json
import joblib
import numpy as np
from azureml.core.model import Model
from my_custom_package.utils.const import MODEL_NAME



# init
# In the init function, the model is deserialised and stored as a global variable. The model storage is mounted to the scoring compute and the path to this model is retrieved in order to deserialise this model.

# run
# Each time the scoring web service is called, the run function is called with the data as a JSON-serialised string.
# This data is then converted to a numpy array and passed to the model for a predictions. The predictions are converted to a list, as the output must be JSON serialisable, and returned from this function.


def init():
    global model
    model_path = Model.get_model_path(MODEL_NAME)
    model = joblib.load(model_path)


def run(data):
    try:
        data = json.loads(data)
        data = data['data']
        result = model.predict(np.array(data))
        return result.tolist()
    except Exception as e:
        error = str(e)
        return error

