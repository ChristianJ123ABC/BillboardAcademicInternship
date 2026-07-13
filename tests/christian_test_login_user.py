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
def test_login_user(client):
    response = client.post("/login", data={
        "email": "fake123@gmail.com",
        "password": "bla!Ammznss$442f4",

    }, follow_redirects = True) #Used to implement redirect responses
    
    assert response.status_code == 200
    assert response.request.path == '/dashboard'







