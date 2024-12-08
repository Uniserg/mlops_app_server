import flask
import logging
from logging.handlers import RotatingFileHandler

from data.models import Salary
from predict_models.salary_model import SalaryModel

salary_model = SalaryModel()

app = flask.Flask(__name__)

# Настройка логирования
handler = RotatingFileHandler('user_requests.log', maxBytes=1000000, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# lab1
@app.route('/api/salary_predict', methods=['POST'])
def get_car_price():
    request_data = flask.request.get_json()
    if not request_data:
        app.logger.info(f"Request: {flask.request.method} {flask.request.url} - No data provided in the request body")
        return flask.jsonify({'error': 'No data provided in the request body'}), 400
    print(request_data)
    salary = Salary.from_json(request_data)
    print(salary)
    salary_predict_value = salary_model.predict(salary)[0]

    response = flask.jsonify({'salary': str(salary_predict_value)})
    response.headers.add('Access-Control-Allow-Origin', '*')

    app.logger.info(f"Request: {flask.request.method} {flask.request.url} - Data: {request_data} - Response: {response.get_json()}")
    return response

if __name__ == '__main__':
   # Запуск Flask-приложения с определенным адресом и портом
   app.run(host='localhost', port=5000, debug=True)
