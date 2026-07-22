#Resources
#https://flask.palletsprojects.com/en/stable/testing/
#https://www.youtube.com/watch?v=RLKW7ZMJOf4&t=595s
#https://flask.palletsprojects.com/en/stable/config/
#https://docs.pytest.org/en/6.2.x/fixture.html
#https://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python
#https://pytutorial.com/python-bytesio-working-with-binary-data-in-memory/
#https://www.geeksforgeeks.org/dbms/querying-data-from-a-database-using-fetchone-and-fetchall/

#Finding time difference from start to completion
#https://www.geeksforgeeks.org/python/time-perf_counter-function-in-python/


import pytest
from server import app as create_app
from pathlib import Path
import MySQLdb
import os
from dotenv import load_dotenv
import base64

import time

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

#NFR5-1
def test_dashboard_loads_under_3_seconds(client):
    with client.session_transaction() as session:
        session["user_id"] = 1

    timeStart = time.perf_counter()
    response = client.get("/dashboard")
    timeEnd = time.perf_counter() - timeStart
    print(timeEnd)

    assert response.status_code == 200
    assert timeEnd < 3.0

#NFR5-2 Rate Limit = 10 times per minute
#WILL PASS ONLY IF RATE LIMITING IS TURNED ON
def test_login_rate_11_times(client):
    for _ in range (11):
        response = client.post("/login", data={
            "email": "fakeemail",
            "password": "fake123"
        })

    assert response.status_code == 429