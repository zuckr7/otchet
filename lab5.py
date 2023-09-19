from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database'
db = SQLAlchemy(app)

class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

class Service(db.Model):
    service_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

@app.route('/clients', methods=['GET', 'POST'])
def manage_clients():
    if request.method == 'GET':
        clients = Client.query.all()
        return jsonify([client.__dict__ for client in clients])
    elif request.method == 'POST':
        data = request.get_json()
        new_client = Client(name=data['name'], email=data['email'])
        db.session.add(new_client)
        db.session.commit()
        return jsonify({'message': 'Client created successfully'})

@app.route('/services', methods=['GET', 'POST'])
def manage_services():
    if request.method == 'GET':
        services = Service.query.all()
        return jsonify([service.__dict__ for service in services])
    elif request.method == 'POST':
        data = request.get_json()
        new_service = Service(name=data['name'], description=data['description'])
        db.session.add(new_service)
        db.session.commit()
        return jsonify({'message': 'Service created successfully'})

if __name__ == '__main__':
    app.run(debug=True)