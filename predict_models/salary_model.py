from data.models import Salary

import pickle
from preprocessing import *


model_path = 'assets/lasso_model.pkl'

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
        df = convert_salary_to_df(salary)
        preprocessed_data = preprocess_data(df)
        return self.model.predict(preprocessed_data)
