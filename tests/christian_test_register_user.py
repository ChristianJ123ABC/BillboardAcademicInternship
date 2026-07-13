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

#Tests to see if an account is created successfully with the correct formats
def test_create_user_account(client):
    response = client.post("/register", data={
        "firstName": "test",
        "lastName": "ting",
        "email": "usertesting@gmail.com",
        "password": "ThisIsATesting12345!",
        "businessName": "Testing Incorporated"

    }, follow_redirects = True) #Used to implement redirect responses

    assert response.status_code == 200
    assert b"Account Created Successfully!" in response.data
    assert response.request.path == '/register'





#EXCEPTION FLOWS

#Tests to see if the email format is invalid
def test_invalid_email_format(client):
    response = client.post("/register", data={
        "firstName": "test",
        "lastName": "ting",
        "email": "invalidemail",
        "password": "ThisIsATesting12345!",
        "businessName": "Testing Incorporated"

    }, follow_redirects = True) 

    assert response.status_code == 200
    assert b"Invalid Email Format, use the following (email@domain.com / name.last@domain.co.uk)" in response.data
    assert response.request.path == '/register'



#Tests to see if the email alreadys exists
def test_already_existing_email(client):
    response = client.post("/register", data={
        "firstName": "test",
        "lastName": "ting",
        "email": "fake123@gmail.com",
        "password": "ThisIsATesting12345!",
        "businessName": "Testing Incorporated"

    }, follow_redirects = True) 

    assert response.status_code == 200
    assert b"Email is already registered" in response.data
    assert response.request.path == '/register'




#INDIVIDUAL TESTS FOR PASSWORD COMPLEXITY

#Tests to see if the password is missing a number
def test_password_missing_number(client):
    response = client.post("/register", data={
        "firstName": "test",
        "lastName": "ting",
        "email": "usertesting23@gmail.com",
        "password": "ImMissingANumber!",
        "businessName": "Testing Incorporated"

    }, follow_redirects = True) 

    assert response.status_code == 200
    assert b"Password has to contain atleast 1 number." in response.data
    assert response.request.path == '/register'
    


#Tests to see if the password is missing a lowercase letter
def test_password_missing_lowercase_letter(client):
    response = client.post("/register", data={
        "firstName": "test",
        "lastName": "ting",
        "email": "usertesting23@gmail.com",
        "password": "IMMISSINGALOWERCASELETTER1!",
        "businessName": "Testing Incorporated"

    }, follow_redirects = True) 

    assert response.status_code == 200
    assert b"Password has to contain atleast 1 lowercase letter." in response.data
    assert response.request.path == '/register'


#Tests to see if the password is missing an uppercase letter
def test_password_missing_uppercase_letter(client):
    response = client.post("/register", data={
        "firstName": "test",
        "lastName": "ting",
        "email": "usertesting23@gmail.com",
        "password": "missinganuppercaseletter1!",
        "businessName": "Testing Incorporated"

    }, follow_redirects = True) 

    assert response.status_code == 200
    assert b"Password has to contain atleast 1 uppercase letter." in response.data
    assert response.request.path == '/register'


#Tests to see if the password is missing a special character
def test_password_missing_special_character(client):
    response = client.post("/register", data={
        "firstName": "test",
        "lastName": "ting",
        "email": "usertesting23@gmail.com",
        "password": "MissingASpecialCharacter1",
        "businessName": "Testing Incorporated"

    }, follow_redirects = True)

    assert response.status_code == 200
    assert b"Password has to contain atleast 1 special character." in response.data
    assert response.request.path == '/register'


#Tests to see if the password is too long
def test_password_length_too_long(client):
    response = client.post("/register", data={
        "firstName": "test",
        "lastName": "ting",
        "email": "usertesting23@gmail.com",
        "password": "ThisPasswordIsWayTooLongAndShouldProbablyBeShortened123456789!!!",
        "businessName": "Testing Incorporated"

    }, follow_redirects = True) 

    assert response.status_code == 200
    assert b"This password is too long, it must be between 10 and 30 characters." in response.data
    assert response.request.path == '/register'


#Tests to see if the password is too short
def test_password_length_too_short(client):
    response = client.post("/register", data={
        "firstName": "test",
        "lastName": "ting",
        "email": "usertesting23@gmail.com",
        "password": "Short1!",
        "businessName": "Testing Incorporated"

    }, follow_redirects = True) 
    assert response.status_code == 200
    assert b"This password is too short, it must be between 10 and 30 characters." in response.data
    assert response.request.path == '/register'







#Used to wipe the testing details from the database
@pytest.fixture(scope="session", autouse=True)
def wipe_db():
    yield #Executes the function
    database = MySQLdb.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DB"),
        port=int(os.getenv("MYSQL_PORT"))
    )
    cursor = database.cursor()
    cursor.execute("DELETE FROM users WHERE email = %s", ("usertesting@gmail.com",))
    cursor.connection.commit()

    cursor.close() 
    database.close()