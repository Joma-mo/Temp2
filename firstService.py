from flask import Flask, request
from botocore.exceptions import NoCredentialsError
from storage import s3, LIARA_BUCKET_NAME
from database import db, appDB, Requests
from rabbitMQ import add_to_queue


app = Flask(__name__)


@app.route("/")
def index():
    urls = {"urls": list()}
    for url in app.url_map.iter_rules():
        if '/static/' not in str(url):
            urls["urls"].append(str(url))
    return {"api": "running", **urls}


@app.route("/upload", methods=["POST"])
def upload_file():
    response = {"message": ""}
    file = request.files["file"]
    myEmail = request.form["email"]
    if file:
        try:
            with appDB.app_context():
                req = Requests(email=myEmail)
                db.session.add(req)
                db.session.commit()
                add_to_queue(req.id)
            s3.upload_fileobj(file, LIARA_BUCKET_NAME, str(req.id))
            response["message"] = "Your request has successfully registered!"
        except NoCredentialsError:
            response["message"] = "Liara credentials not found."
            req.status = "Failure"
            db.session.commit()
        except Exception as e:
            response["message"] = str(e)
            req.status = "Failure"
            db.session.commit()
        finally:
            return response
    else:
        response["message"] = "No file selected."


if __name__ == "__main__":
    app.run(debug=True)
