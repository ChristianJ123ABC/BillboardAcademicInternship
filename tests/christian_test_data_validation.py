
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
resources = Path(__file__).parent.parent / "tests" / "resources" #Folder used to hold test files

@pytest.fixture()
def app():
    create_app.config.update({
        "TESTING": True,
        
    })
    yield create_app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_upload_wrong_file_format(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["subscription_plan"] = "Basic"
    
    response = client.post("/uploadAdvertisement", data = {
            "file": (resources / "biometrics.csv").open("rb"),
            "caption": "DELETEME",


    }, follow_redirects = True)

    assert response.status_code == 200
    assert b"Invalid file type, use the following file extensions: png, jpg, jpeg, mp4, mov, mkv" in response.data
    assert response.request.path == '/uploadAdvertisement'

def test_sql_injection(client):
    response = client.post("/login", data = {
        "email": "' OR '1'='1'",
        "password": "' OR '1'='1'"
    })

    assert response.status_code == 200
    assert b"Invalid Email Address or Password. please try again." in response.data