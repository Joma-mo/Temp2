import os
import sys
import requests
from database import db, appDB, Requests
from rabbitMQ import channel, connection
from storage import s3, LIARA_BUCKET_NAME
from io import BytesIO

shazam_url = "https://shazam-api-free.p.rapidapi.com/shazam/recognize/"


def read_from_queue():
    channel.queue_declare(queue='requests_queue')
    error = {"Message": ""}

    def callback(ch, method, properties, body):
        try:
            print(int(body))
            requestID = str(int(body))
            response = s3.get_object(Bucket=LIARA_BUCKET_NAME, Key=requestID)
            audio_content = response['Body'].read()

            payload = {
                "upload_file": (requestID + '.mp3', BytesIO(audio_content))
            }
            headers = {
                "X-RapidAPI-Key": "735946fef0msh2afbf4744f57759p17b255jsnd48556b1b192",
                "X-RapidAPI-Host": "shazam-api-free.p.rapidapi.com"
            }
            response = requests.post(shazam_url, files=payload, headers=headers)

            if response.status_code == 200:
                shazam_data = response.json()
                song_title = shazam_data['track']['title']
                print(song_title)
                songID = search_in_spotify(song_title)
                print(songID)
                with appDB.app_context():
                    db.session.query(Requests).filter(Requests.id == requestID).update({"songID": songID, "status":'Ready'})
                    db.session.commit()
            else:
                print(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            error["Message"] = str(e)
        finally:
            return error

    # Start consuming messages
    channel.basic_consume(queue='requests_queue', on_message_callback=callback, auto_ack=True)

    print("Waiting for messages. To exit, press CTRL+C")
    channel.start_consuming()

    # Close the connection
    connection.close()


def search_in_spotify(song_name):
    spotify_url = "https://spotify23.p.rapidapi.com/search/"

    querystring = {"q": song_name, "type": "tracks", "offset": "0", "limit": "10",
                   "numberOfTopResults": "5"}

    headers = {
        "X-RapidAPI-Key": "735946fef0msh2afbf4744f57759p17b255jsnd48556b1b192",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    response = requests.get(spotify_url, headers=headers, params=querystring)

    if response.status_code == 200:
        response_json = response.json()
        spotify_id = response_json['tracks']['items'][0]['data']['id']
        return spotify_id
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


if __name__ == '__main__':
    try:
        read_from_queue()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
