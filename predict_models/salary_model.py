from data.models import Salary

import pickle
import pandas as pd
import random
from sklearn.preprocessing import StandardScaler

numeric_data = ['Age', 'Experience', 'Salary']
categorical_data = ['Gender', 'Education', 'Location', 'Job_Title']
numeric_features = ['Age', 'Experience']

dimension_data = ['Gender', 'Location', 'Job_Title']

features = ['Education', 'Experience', 'Location', 'Job_Title', 'Age', 'Gender']
target = 'Salary'


def convert_salary_to_df(salary: Salary):
    return pd.DataFrame([salary.to_json()])


def preprocess_data(data):
    preprocessed_data = pd.DataFrame()
    one_hot_df = pd.get_dummies(data[dimension_data], drop_first=True, dtype=int)
    education_order = {'High School': 0, 'Bachelor': 1, 'Master': 2, 'PhD': 3}
    preprocessed_data['Education'] = data['Education'].map(education_order)
    # Масштабирование числовых данных
    scaler = StandardScaler()
    preprocessed_data[numeric_features] = scaler.fit_transform(data[numeric_features])
    
    to_concat = [preprocessed_data, one_hot_df]

    if target in data.columns:
        to_concat.append(data[target])
    
    preprocessed_data = pd.concat(to_concat, axis=1)
    
    return preprocessed_data


class SalaryModel:
    def load_model(self):
        with open('assets/model.pkl', 'rb') as file:
            loaded_model = pickle.load(file)
        return loaded_model

    def predict(self, salary: Salary) -> float:
        # Реализовать модель машинного обучения
        df = convert_salary_to_df(salary)
        model = self.load_model()
        print('df = ', df)
        print('tsa', preprocess_data(df))
        return model.predict(preprocess_data(df))
