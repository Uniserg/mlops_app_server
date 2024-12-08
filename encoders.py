import pandas as pd

class EducationEncoder:
  def __init__(self) -> None:
     self.education_order = {'High School': 0, 'Bachelor': 1, 'Master': 2, 'PhD': 3}
     self.categories = 'Education'

  def transform(self, data: pd.DataFrame):
    return data['Education'].map(self.education_order)

  def __repr__(self) -> str:
    return "EducationEncoder()"

  def fit(self, _):
    pass