import os
import joblib
from azureml.core import Datastore, Dataset, Run
from sklearn.metrics import mean_squared_error ,mean_absolute_error
# My custome files
from Preprocessing_and_model_pipline import preprocessing_and_model_pipline
from get_data import get_df_from_datastore_path
from my_custom_package.utils.const import TRAINING_DATASTORE, MODEL_NAME




__here__ = os.path.dirname(__file__)



def prepare_data(workspace):
    datastore = Datastore.get(workspace, TRAINING_DATASTORE)
    data = get_df_from_datastore_path(datastore, "sample_data.csv")
    data_x = data.drop(['Occupancy_Rate'], axis=1) # drop labels for training set
    data_y = data['Occupancy_Rate'].copy()
    X_train, X_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.3)
    return x_train, y_train, x_test, y_test


def train_model(x_train, y_train):
    return (preprocessing_and_model_pipline.fit(X_train,y_train))


def evaluate_model(trained_model, x_test, y_test):
    y_pred=trained_model.predict(x_test)
    mean_squared_error = mean_squared_error(y_test, y_pred) ** 0.5
    run.log('mean_squared_error', mean_squared_error)


def save_model(trained_model):
    output_dir = os.path.join(__here__, 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, 'model.pkl')
    joblib.dump(trained_model, model_path)
    return model_path


def register_model(run, model_path):
    run.upload_file(model_path, "outputs/model.pkl")
    model = run.register_model(
        model_name=MODEL_NAME,
        model_path="outputs/model.pkl"
    )
    run.log('Model_ID', model.id)

    
def main():
    run = Run.get_context()
    workspace = run.experiment.workspace
    x_train, y_train, x_test, y_test = prepare_data(workspace)
    trained_model = train_model(x_train, y_train)
    evaluate_model(trained_model, x_test, y_test)
    model_path = save_model(trained_model)
    register_model(run, model_path)


if __name__ == '__main__':
    main()








