import json
from preprocessing import *
from data.models import Salary

class CustomSalaryModel:
    def __init__(self) -> None:
        self.weights, self.bias = CustomSalaryModel._load_weights()

    @staticmethod
    def _load_weights():
        with open("assets/model_weights.json", "r") as f:
            data = json.load(f)
            return data["weights"], data["bias"]
        
    def predict(self, salary: Salary) -> float:
        df = convert_salary_to_df(salary)
        preprocessed_data = preprocess_data(df)
        return self.predict_with_X(preprocessed_data)

    def predict_with_X(self, X) -> float:
        return sum(w * x for w, x in zip(self.weights, X)) + self.bias

    