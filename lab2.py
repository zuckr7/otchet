from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

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

class Request(db.Model):
    request_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
    request_date = db.Column(db.Date)
    status = db.Column(db.String(50))

@app.route('/clients', methods=['GET', 'POST'])
def manage_clients():
    if request.method == 'GET':
        clients = Client.query.all()
        return jsonify([client.__dict__ for client in clients])
    elif request.method == 'POST':
        data = request.get_json()
        new_client = Client(name=data['name'], email=data['email'])
        try:
            db.session.add(new_client)
            db.session.commit()
            return jsonify({'message': 'Client created successfully'})
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Client with this email already exists'})

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

@app.route('/requests', methods=['GET', 'POST'])
def manage_requests():
    if request.method == 'GET':
        requests = Request.query.all()
        return jsonify([request.__dict__ for request in requests])
    elif request.method == 'POST':
        data = request.get_json()
        new_request = Request(client_id=data['client_id'], request_date=data['request_date'], status=data['status'])
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'message': 'Request created successfully'})

if __name__ == '__main__':
    app.run(debug=True)
