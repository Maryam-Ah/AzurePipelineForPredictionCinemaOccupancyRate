import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error ,mean_absolute_error

# my custome files
from config import  numerical_featurs,categorical_featurs, model

try:
    from sklearn.impute import SimpleImputer # Scikit-Learn 0.20+
except ImportError:
    from sklearn.preprocessing import Imputer as SimpleImputer
    
    
    
    


#Custom Transformer that extracts columns passed as argument to its constructor 
class FeatureSelector( BaseEstimator, TransformerMixin ):
    #Class Constructor 
    def __init__( self, feature_names ):
        self._feature_names = feature_names 
    
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self 
    
    #Method that describes what we need this transformer to do
    def transform( self, X, y = None ):
        return X[ self._feature_names ] 
    
    
    
    
    
class NumericalTransformer(BaseEstimator, TransformerMixin):
    #Class Constructor
    def __init__( self, Presales = True ):
        self.Presales = Presales

        
    #Return self, nothing else to do here
    def fit( self, X, y = None ):
        return self 
    
    #Custom transform method we wrote that add 1 to each single values of Presales feature.
    def transform(self, X, y = None):
        #Check if needed 
        if self.Presales:
            #create new column
            X.loc[:,'Presales'] = X['Presales'] +1
        return X.values




def preprocessing_and_model_pipline(X_train,y_train):
    
    # Pipline for numerical featurs
    num_pipeline = Pipeline(steps=[
                           ( 'num_selector', FeatureSelector(numerical_featurs) ),
                           ( 'num_transformer', NumericalTransformer() ),
                           ('imputer', SimpleImputer(strategy='median')),
                           ('scaler', StandardScaler())])
    
    
    # Pipline for categorical featurs
    cat_pipeline = Pipeline(steps=[
                           ( 'cat_selector', FeatureSelector(categorical_featurs) ),
                           ('imputer', SimpleImputer(strategy='constant', fill_value ='missing_value')),
                           ('encoder', OneHotEncoder(drop='if_binary',handle_unknown='error') )])
    
    
    # Pipline for preprocessing the data
    full_pipeline = FeatureUnion (transformer_list = [ ( 'categorical_pipeline', cat_pipeline ), 
                                                       ( 'numerical_pipeline', num_pipeline ) ] )
    
    


    # Full pipline
    model_pipeline = Pipeline(steps=[ 
                                 ('pre_processing',full_pipeline),
                                 ('model_name', model)
                                 ])


    return (model_pipeline)

