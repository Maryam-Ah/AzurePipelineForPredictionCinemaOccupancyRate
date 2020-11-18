import numpy as np
import pandas as pd
import seaborn as sns
import lightgbm as lgb


# Identify Categorical featurs
def categorical_featurs():
    categorical_featurs = ["Location_ID",
                       "Auditorium_Type",
                       "Language",
                       "Business_Day",
                       "Is_Holiday",
                       "Genre",
                       "Rating",
                       "Awards"]
    return(categorical_featurs)


# Identify Numerical featurs
def numerical_featurs():
    numerical_featurs = ['Weeks_Since_Release', 'Runtime', 'Business_Week_Of_Year', 'Presales']
    return(numerical_featurs)
    

# Define the model name 
def model():
    model = lgb.LGBMRegressor()
    return (model)






