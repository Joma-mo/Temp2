from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

appDB = Flask(__name__)

dbname = "postgres"
user = "root"
password = "oVMYwFkX7EVnjABCZaGZTVlI"
host = "manaslu.liara.cloud"
port = "32081"

database_url = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
appDB.config['SQLALCHEMY_DATABASE_URI'] = database_url

# Creating an SQLAlchemy instance
db = SQLAlchemy(appDB)

with appDB.app_context():
    class Requests(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        email = db.Column(db.String(100), nullable=False)
        status = db.Column(db.String(20), nullable=False, server_default="pending")
        songID = db.Column(db.String(100), nullable=True)

        def __repr__(self):
            return f"ID: {self.id}, Email: {self.email}, Status: {self.status}, songID: {self.songID}"


    # db.create_all()


    # def add_data(myEmail):
    #     req = Requests(email=myEmail)
    #     db.session.add(req)
    #     db.session.commit()


    # users = Requests.query.all()
    # print(users)


