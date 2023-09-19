from spyne import Application, srpc, ServiceBase, Unicode, Integer, DateTime
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask import Flask

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

class DataService(ServiceBase):
    @srpc(Unicode, Unicode, _returns=Integer)
    def add_client(name, email):
        new_client = Client(name=name, email=email)
        try:
            db.session.add(new_client)
            db.session.commit()
            return new_client.client_id
        except IntegrityError:
            db.session.rollback()
            return -1  # Client with this email already exists

    @srpc(Integer, _returns=Unicode)
    def get_client_name(client_id):
        client = Client.query.get(client_id)
        return client.name if client else "Client not found"

    @srpc(Unicode, Unicode, _returns=Integer)
    def add_service(name, description):
        new_service = Service(name=name, description=description)
        db.session.add(new_service)
        db.session.commit()
        return new_service.service_id

    @srpc(Integer, _returns=Unicode)
    def get_service_name(service_id):
        service = Service.query.get(service_id)
        return service.name if service else "Service not found"

if __name__ == '__main__':
    application = Application([DataService],
                              tns='MySOAP',
                              in_protocol=Soap11(validator='lxml'),
                              out_protocol=Soap11())
    wsgi_application = WsgiApplication(application)

    app.run(host='0.0.0.0', port=8080)