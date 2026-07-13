#Resources
#https://flask.palletsprojects.com/en/stable/testing/
#https://www.youtube.com/watch?v=RLKW7ZMJOf4&t=595s
#https://flask.palletsprojects.com/en/stable/config/
#https://docs.pytest.org/en/6.2.x/fixture.html
#https://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python



import pytest
from server import app as create_app
from pathlib import Path



@pytest.fixture()
def app():
    create_app.config.update({
        "TESTING": True,
        
    })
    yield create_app

@pytest.fixture()
def client(app):
    return app.test_client()


#NORMAL FLOWS
#Tests to see if the user is logged into the dashboard
def test_login_user(client):
    response = client.post("/login", data={
        "email": "fake123@gmail.com",
        "password": "bla!Ammznss$442f4"

    }, follow_redirects = True) #Used to implement redirect responses
    
    assert response.status_code == 200
    assert response.request.path == '/dashboard'




#EXCEPTION FLOWS
#Tests if the users password is wrong.
def test_login_password_invalid(client):
    response = client.post("/login", data={
        "email": "fake123@gmail.com",
        "password": "wrongpassword"

    })
    
    assert response.status_code == 200
    assert b"Invalid Email Address or Password. please try again." in response.data


def test_login_email_invalid(client):
#Same test result as above except wrong email
    response = client.post("/login", data={
        "email": "wrongemail@gmail.com",
        "password": "bla!Ammznss$442f4"

    })
    
    assert response.status_code == 200
    assert b"Invalid Email Address or Password. please try again." in response.data










