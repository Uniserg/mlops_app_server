from data.models import Salary

import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from encoders import EducationEncoder


numeric_data = ['Age', 'Experience', 'Salary']
categorical_data = ['Gender', 'Education', 'Location', 'Job_Title']
numeric_features = ['Age', 'Experience']

ordering_data = ['Education']
dimension_data = ['Gender', 'Location', 'Job_Title']

features = ['Education', 'Experience', 'Location', 'Job_Title', 'Age', 'Gender']
target = 'Salary'


def _load_encoders():
    with open('assets/encoders.pkl', 'rb') as file:
        loaded_encoders = pickle.load(file)
    return loaded_encoders

encoders = _load_encoders() 


def create_encoder_by_feature(feature):
  if feature in numeric_data:
    return StandardScaler()
  elif feature in dimension_data:
    return OneHotEncoder(sparse_output=False)
  elif feature == 'Education':
    return EducationEncoder()
  
  return None
  
def create_feature_encoders(data):
  encoders = {}
  
  for feature in data.columns:
    encoder = create_encoder_by_feature(feature)
    encoder.fit(data[[feature]])
    encoders[feature] = encoder

  return encoders

def get_encoded_data(data, encoder, column) -> pd.DataFrame:
  if hasattr(encoder, 'categories_'):
    columns = encoder.categories_
  else:
    columns = [column]
  
  return pd.DataFrame(encoder.transform(data), columns=columns)

def convert_salary_to_df(salary: Salary):
    return pd.DataFrame([salary.to_json()])

def preprocess_data(data):
    if 'Salary' in data.columns:
       data = data.drop(['Salary'], axis=1)

    preprocessed_data = pd.DataFrame()
    for feature, encoder in encoders.items():
      if feature not in data.columns:
         continue
      encoded_data = get_encoded_data(data[[feature]], encoder, feature)
      preprocessed_data = pd.concat([preprocessed_data, encoded_data], axis=1)
      preprocessed_data.columns = preprocessed_data.columns.astype(str)
    
    return preprocessed_data