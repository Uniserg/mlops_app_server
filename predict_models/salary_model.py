from data.models import Salary

import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from encoders import EducationEncoder


model_path = 'assets/lasso_model.pkl'

numeric_data = ['Age', 'Experience', 'Salary']
categorical_data = ['Gender', 'Education', 'Location', 'Job_Title']
numeric_features = ['Age', 'Experience']

ordering_data = ['Education']
dimension_data = ['Gender', 'Location', 'Job_Title']

features = ['Education', 'Experience', 'Location', 'Job_Title', 'Age', 'Gender']
target = 'Salary'

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


def preprocess_data(data, encoders):
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

class SalaryModel:

    def __init__(self) -> None:
        self.model = SalaryModel._load_model()
        self.encoders = SalaryModel._load_encoders()

    @staticmethod
    def _load_encoders():
        with open('assets/encoders.pkl', 'rb') as file:
            loaded_encoders = pickle.load(file)
        return loaded_encoders
    
    @staticmethod
    def _load_model():
        with open(model_path, 'rb') as file:
            loaded_model = pickle.load(file)
        return loaded_model

    def predict(self, salary: Salary) -> float:
        # Реализовать модель машинного обучения
        df = convert_salary_to_df(salary)
        preprocessed_data = preprocess_data(df, self.encoders)
    
        print("tsa:")
        print(preprocessed_data)
        return self.model.predict(preprocessed_data)
