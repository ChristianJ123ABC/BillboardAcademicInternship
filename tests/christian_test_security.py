
#Resources
#https://flask.palletsprojects.com/en/stable/testing/
#https://www.youtube.com/watch?v=RLKW7ZMJOf4&t=595s
#https://flask.palletsprojects.com/en/stable/config/
#https://docs.pytest.org/en/6.2.x/fixture.html
#https://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python
#https://pytutorial.com/python-bytesio-working-with-binary-data-in-memory/
#https://www.geeksforgeeks.org/dbms/querying-data-from-a-database-using-fetchone-and-fetchall/


import pytest
from server import app as create_app
from pathlib import Path
import MySQLdb
import os
from dotenv import load_dotenv
import base64


load_dotenv(override=True)


@pytest.fixture()
def app():
    create_app.config.update({
        "TESTING": True,
        
    })
    yield create_app

@pytest.fixture()
def client(app):
    return app.test_client()

#NFR1-1
def test_check_user_password_is_hashed(client):
    database = MySQLdb.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DB"),
        port=int(os.getenv("MYSQL_PORT")),
        charset=os.getenv("MYSQL_CHARSET")
    )
    cursor = database.cursor()
    cursor.execute("SELECT hashed_password from users WHERE email = %s", ("fake123@gmail.com",)) 
    passwordCheck = cursor.fetchone()
    cursor.close()
    database.close()

    assert passwordCheck[0].startswith(("scrypt")) #Hashed passwords start with scrypt


#NFR1-2
def test_secret_key_length(client):
    secret_key = os.getenv("SECRET_KEY") 
    decodedKey = base64.b64decode(secret_key)
    assert len(decodedKey) >= 32 #A good secret key is base 64 and when decoded it is greater than 32 bytes.

#NFR1-3
def test_user_tries_to_access_dashboard_early(client):
   response = client.post("/login", data={
        "email": "2FAenabled@gmail.com", #Account with 2FA Enabled
        "password": "DoNotTouch2FA123!!!"

    }, follow_redirects = True) #Used to implement redirect responses
   
   assert response.status_code == 200
   assert response.request.path != '/dashboard' #Checks to see if the user is NOT sent to the dashboard immediately, which they aren't since 2FA is enabled

#NFR1-4
def test_delete_file_not_owned(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
    
    response = client.get("/deleteFile/10049", follow_redirects=True)

    assert response.status_code == 200
    assert b"You are trying to delete a file that does not belong to you." in response.data
    assert response.request.path == '/dashboard'



