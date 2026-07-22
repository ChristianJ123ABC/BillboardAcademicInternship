
#Resources
#https://flask.palletsprojects.com/en/stable/testing/
#https://www.youtube.com/watch?v=RLKW7ZMJOf4&t=595s
#https://flask.palletsprojects.com/en/stable/config/
#https://docs.pytest.org/en/6.2.x/fixture.html
#https://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python
#https://pytutorial.com/python-bytesio-working-with-binary-data-in-memory/


import pytest
from server import app as create_app
from pathlib import Path
import MySQLdb
import os
from dotenv import load_dotenv
import shutil #Used to copy files from backup folder when deleting files
import io #Used to print an empty file object to replicate no file selected

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

#NFR3-1
def test_404_error_handled(client):
    response = client.get("/PageDoesnotExist10123012")

    assert response.status_code == 404
    assert b"404 Page not found! Please try a new page"

#NFR3-2
def test_invalid_input_for_login(client):
     response = client.post("/login", data={
            "email": "fake123@gmail.com",
            "password": "wrongpassword"
    
        })
     assert response.status_code == 200
     assert b"Invalid Email Address or Password. please try again." in response.data