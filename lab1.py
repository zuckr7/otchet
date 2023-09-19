from flask import Flask, request
import math
import datetime

app = Flask(__name__)

@app.route('/number_to_words/<int:number>', methods=['GET'])
def number_to_words(number):
    return "Результат: " + str(number)

@app.route('/solve_equation', methods=['GET'])
def solve_equation():
    a = float(request.args.get('a'))
    b = float(request.args.get('b'))
    c = float(request.args.get('c'))

    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        return f"Решения: x1={x1}, x2={x2}"
    elif discriminant == 0:
        x1 = x2 = -b / (2*a)
        return f"Единственное решение: x1=x2={x1}"
    else:
        return "Нет действительных корней"

@app.route('/get_day_of_week', methods=['GET'])
def get_day_of_week():
    date_str = request.args.get('date')
    date_obj = datetime.datetime.strptime(date_str, '%d.%m.%Y')
    day_of_week = date_obj.strftime('%A')
    return f"День недели: {day_of_week}"

@app.route('/fibonacci/<int:index>', methods=['GET'])
def fibonacci(index):

    return "Результат: " + str(index)

@app.route('/get_region_name/<int:region_code>', methods=['GET'])
def get_region_name(region_code):

    return "Результат: " + str(region_code)

if __name__ == '__main__':
    app.run(debug=True)