class Salary:
    def __init__(self, age=None, 
                 gender=None, 
                 job_title=None, 
                 education=None, 
                 experience=None, 
                 location=None,
                 salary=None):
        self.age = age
        self.gender = gender
        self.job_title = job_title
        self.education = education
        self.experience = experience
        self.location = location
        self.salary = salary

    def to_json(self):
        return {
            'Age': self.age,
            'Gender': self.gender,
            'Job_Title': self.job_title,
            'Education': self.education,
            'Experience': self.experience,
            'Location': self.location,
            'Salary': self.salary,
        }

    @classmethod
    def empty(cls):
        return cls()

    @classmethod
    def from_json(cls, json_data):
        return cls(
            age=json_data.get('age', -1),
            gender=json_data.get('gender', ""),
            job_title=json_data.get('jobTitle', ""),
            education=json_data.get('educationLevel', ""),
            experience=float(json_data.get('yearsOfExperience', 0)),
            location=json_data.get("location", ""),
            salary=json_data.get('salary', 0)
        )

    def __str__(self):
        return (f'Salary(age: {self.age}, gender: {self.gender}, jobTitle: {self.job_title}, '
                f'educationLevel: {self.education}, yearsOfExperience: {self.experience}, '
                f'salary: {self.salary})')
