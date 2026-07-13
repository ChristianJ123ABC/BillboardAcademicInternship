#Resources
#https://flask.palletsprojects.com/en/stable/testing/
#https://www.youtube.com/watch?v=RLKW7ZMJOf4&t=595s
#https://flask.palletsprojects.com/en/stable/config/
#https://docs.pytest.org/en/6.2.x/fixture.html
#https://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python



import pytest
from server import app as create_app
from pathlib import Path

#Tests to see if the user is redirected to the 2FA screen when it is enabled
def test_login_redirects_user_to_2fa(client):
    response = client.post("/login", data={
        "email": "2FAenabled@gmail.com", #Account with 2FA Enabled
        "password": "DoNotTouch2FA123!!!"

    }, follow_redirects = True) #Used to implement redirect responses
    
    assert response.status_code == 200
    assert response.request.path == '/login/2fa'

@pytest.mark.xfail(reason="impossible to use the same TOTP code")
#Given the code is correct, the user should be logged into once the TOTP is valid.
def test_login_TOTP_valid(client):
    with client.session_transaction() as session: #Provides session data to bypass certain pages
        session["pending_user_id"] = 14
        session["pending_firstName"] = "2FA"
        session["pending_lastName"] = "Enabled"
        session["pending_businessName"] = "2FAEnterprises"
        session["pending_email"] = "2FAenabled@gmail.com"

    response = client.post("/login/2fa", data={
        "code": 123456

    }, follow_redirects = True)
    
    assert response.status_code == 200
    assert b"Login Successful!" in response.data
    assert response.request.path == '/dashboard'


def test_login_TOTP_invalid(client):
#Tests to see if the TOTP 2FA code is invalid
    with client.session_transaction() as session: #Provides session data to bypass certain pages
        session["pending_user_id"] = 14
        session["pending_firstName"] = "2FA"
        session["pending_lastName"] = "Enabled"
        session["pending_businessName"] = "2FAEnterprises"
        session["pending_email"] = "2FAenabled@gmail.com"

    response = client.post("/login/2fa", data={
        "code": 2

    })
    
    assert response.status_code == 200
    assert b"Invalid code." in response.data
