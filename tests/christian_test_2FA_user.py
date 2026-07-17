#Resources
#https://flask.palletsprojects.com/en/stable/testing/
#https://www.youtube.com/watch?v=RLKW7ZMJOf4&t=595s
#https://flask.palletsprojects.com/en/stable/config/
#https://docs.pytest.org/en/6.2.x/fixture.html
#https://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python



import pytest
from server import app as create_app
from pathlib import Path
import MySQLdb
import os
from dotenv import load_dotenv

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



#NORMAL FLOWS
#UC3-1
def test_setup_2fa_generates_qr_code(client):
    with client.session_transaction() as session:
        session["user_id"] = 1 #Account with 2FA Disabled
        session["email"] = "fake123@gmail.com"

    response = client.get("/setup2FA")
    assert response.status_code == 200
    assert b"data:image/png" in response.data 

#UC3-2
@pytest.mark.xfail(reason="impossible to use the same TOTP code")
def test_enable_2fa(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["email"] = "fake123@gmail.com"
        session["2fa_secret"] = "gAAAAABqV8XSl36TqlT9npZiGEeadkkpwz-URfsKNn5-P13GPWh1klIya9t9Nwrn6l8fzNiDzpX1KC9EHjqe54FeIuy_bHeHfQ8e7RSV1Dq0OK-w-rIPsVv9GC6wv5LTwRq8JUquvhKV"

    response = client.post("/setup2FA/verify", data={
        "code": 123456

    }, follow_redirects = True)

    assert response.status_code == 200
    assert b"2FA has been enabled!" in response.data
    assert response.request.path == '/dashboard'


#ALTERNATE FLOWS
#UC3-3
@pytest.mark.xfail(reason="impossible to use the same TOTP code")
def test_disable_2fa(client):
    with client.session_transaction() as session:
        session["user_id"] = 14
        session["email"] = "2FAenabled@gmail.com" #Account with 2FA Enabled
        session["2fa_secret"] = "gAAAAABqVRvNAC_8ZbFC_GouvHK0pngoSFOAs2GGn2cxGfCz4E2CWxvUK4Gqx9UjljiqQYQ0h1ij5o-MMW5DTZNoiC9Ic9m2kQBg3SnWGofISKNmUWU-KwGiS8yYcRfVyef9dTn-s5L_"

    response = client.post("/disable2FA/deactivate", data={
        "code": 123456

    }, follow_redirects = True)

    assert response.status_code == 200
    assert b"2FA disabled. We recommend you remove your authenticator account since it is now invalid." in response.data
    assert response.request.path == '/dashboard'



#EXCEPTION FLOWS
#UC3-4
def test_2fa_already_enabled(client):
    with client.session_transaction() as session:
        session["user_id"] = 14
        session["email"] = "2FAenabled@gmail.com"
        session["2fa_secret"] = "gAAAAABqVRvNAC_8ZbFC_GouvHK0pngoSFOAs2GGn2cxGfCz4E2CWxvUK4Gqx9UjljiqQYQ0h1ij5o-MMW5DTZNoiC9Ic9m2kQBg3SnWGofISKNmUWU-KwGiS8yYcRfVyef9dTn-s5L_"

    response = client.get("/setup2FA", follow_redirects=True)

    assert response.status_code == 200
    assert b"2FA is already enabled" in response.data
    assert response.request.path == '/dashboard'

#UC3-5
def test_2fa_verification_code_invalid(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["email"] = "fake123@gmail.com"
        session["2fa_secret"] = "gAAAAABqV8XSl36TqlT9npZiGEeadkkpwz-URfsKNn5-P13GPWh1klIya9t9Nwrn6l8fzNiDzpX1KC9EHjqe54FeIuy_bHeHfQ8e7RSV1Dq0OK-w-rIPsVv9GC6wv5LTwRq8JUquvhKV"

    response = client.post("/setup2FA/verify", data={
        "code": 0

    }, follow_redirects = True)

    assert response.status_code == 200
    assert b"Invalid code. Try again." in response.data
    assert response.request.path == '/setup2FA'

#UC3-6
def test_2fa_disable_code_invalid(client):
     with client.session_transaction() as session:
       session["user_id"] = 14
       session["email"] = "2FAenabled@gmail.com"
       session["2fa_secret"] = "gAAAAABqVRvNAC_8ZbFC_GouvHK0pngoSFOAs2GGn2cxGfCz4E2CWxvUK4Gqx9UjljiqQYQ0h1ij5o-MMW5DTZNoiC9Ic9m2kQBg3SnWGofISKNmUWU-KwGiS8yYcRfVyef9dTn-s5L_"

     response = client.post("/disable2FA/deactivate", data={
        "code": 0

     }, follow_redirects = True)

     assert response.status_code == 200
     assert b"Invalid code." in response.data
     assert response.request.path == '/disable2FA'


