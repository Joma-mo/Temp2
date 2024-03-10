import schedule
import time
import requests
from database import db, appDB, Requests

MAILGUN_API_KEY = "be88f271c5cd3cafd1cf3e623d9d9d27-2c441066-b57c101b"git 
MAILGUN_DOMAIN = 'your_mailgun_domain'
MAILGUN_SENDER = 'your_email@example.com'
def send_email():
    with appDB.app_context():
        ready_requests = db.session.query(Requests).filter(Requests.status == "Ready").all()
        for req in ready_requests:
            print(req)
            songID = req.songID
            url = "https://spotify23.p.rapidapi.com/recommendations/"

            params = {
                "limit": "5", "seed_tracks": songID
            }

            headers = {
                "X-RapidAPI-Key": "735946fef0msh2afbf4744f57759p17b255jsnd48556b1b192",
                "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=params)


            if response.status_code == 200:
                suggestions = response.json()['tracks']
                print(suggestions)
                user_email = req.email

                # send_email(user_email, suggestions)
                # req.status = 'done'
                # db.session.commit()


send_email()

# schedule.every(10).seconds.do(my_method)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
