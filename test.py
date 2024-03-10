import psycopg2

db_connection = psycopg2.connect(
    dbname="postgres",
    user="root",
    password="oVMYwFkX7EVnjABCZaGZTVlI",
    host="manaslu.liara.cloud",
    port="32081"
)
myEmail = 'allggiii@gmail.com'

cursor = db_connection.cursor()

cursor.execute("select * from Requests;")
info = cursor.fetchall()
print(info)
db_connection.close()

# import requests
#
# shazam_url = "https://shazam-api-free.p.rapidapi.com/shazam/recognize/"
# file_path = "song.mp3"
# file = open(file_path, "rb")
# file_content = file.read()
# payload = {
#     "upload_file": (file_path, file_content)
# }
# headers = {
#     "X-RapidAPI-Key": "735946fef0msh2afbf4744f57759p17b255jsnd48556b1b192",
#     "X-RapidAPI-Host": "shazam-api-free.p.rapidapi.com"
# }
# response = requests.post(shazam_url, files=payload, headers=headers)
#
# print(response.json())

# from database import db, appDB, Requests
#
# filename = 1
# songID = 'sdjl8934'
#
# with appDB.app_context():
#     db.session.query(Requests).filter(Requests.id == filename).update({"songID": songID, "status": 'Ready'})
#     db.session.commit()
