from flask import Flask, jsonify
import requests

app = Flask(__name__)


# Функция для вызова REST API и замены пробелов на нижнее подчёркивание
def call_external_api():
    api_url = "http://www.mocky.io/v2/5c7db5e13100005a00375fda"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict):
            modified_data = {}
            for key, value in data.items():
                modified_key = key.replace(" ", "_")
                modified_data[modified_key] = value
            return modified_data
    return None


@app.route('/get_modified_data', methods=['GET'])
def get_modified_data():
    modified_data = call_external_api()
    if modified_data:
        return jsonify(modified_data)
    else:
        return jsonify({'error': 'Failed to fetch and modify data from external API'})


if __name__ == '__main__':
    app.run(debug=True)