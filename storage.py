import os
import boto3
# from flask import Flask, request
# from botocore.exceptions import NoCredentialsError
# from urllib.parse import quote
# from database import db, pro, Requests
# from rabbitMQ import RabbitMQ

LIARA_ENDPOINT = "https://storage.iran.liara.space"
LIARA_BUCKET_NAME = "hw1-bucket"
LIARA_ACCESS_KEY = "n9dg0it3n3mruv6q"
LIARA_SECRET_KEY = "109dae20-be7b-4caa-94d7-b93013b8db78"

s3 = boto3.client(
    "s3",
    endpoint_url=LIARA_ENDPOINT,
    aws_access_key_id=LIARA_ACCESS_KEY,
    aws_secret_access_key=LIARA_SECRET_KEY,
)

#
# app = Flask(__name__)
#
#
# @app.route("/")
# def index():
#     urls = {"urls": list()}
#     for url in app.url_map.iter_rules():
#         if '/static/' not in str(url):
#             urls["urls"].append(str(url))
#     return {"api": "running", **urls}
#
#
# @app.route("/upload", methods=["POST"])
# def upload_file():
#     response = {"message": ""}
#     file = request.files["file"]
#     myEmail = request.form["email"]
#     if file:
#         try:
#             with pro.app_context():
#                 req = Requests(email=myEmail)
#                 db.session.add(req)
#                 db.session.commit()
#                 RabbitMQ.add_to_queue(req.id)
#             s3.upload_fileobj(file, LIARA_BUCKET_NAME, file.filename)
#             response["message"] = "Your request has successfully registered!"
#         except NoCredentialsError:
#             response["message"] = "Liara credentials not found."
#             req.status = "Failure"
#             db.session.commit()
#         except Exception as e:
#             response["message"] = str(e)
#             req.status = "Failure"
#             db.session.commit()
#         finally:
#             return response
#     else:
#         response["message"] = "No file selected."
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
