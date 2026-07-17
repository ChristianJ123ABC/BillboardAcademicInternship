
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

#NORMAL FLOW
#UC5-1
def test_access_upload_page_subscribed(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["subscription_plan"] = "Basic"
    
    response = client.get("/uploadAdvertisement")
    assert response.status_code == 200

#UC5-2
def test_upload_advertisement_image(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["subscription_plan"] = "Basic"
    
    response = client.post("/uploadAdvertisement", data = {
            "file": (resources / "smiley.jpg").open("rb"),
            "caption": "DELETEME",


    }, follow_redirects = True)

    assert response.status_code == 200
    assert b"File uploaded successfully" in response.data
    assert response.request.path == '/uploadAdvertisement'

#UC5-3
def test_upload_advertisement_video(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["subscription_plan"] = "Basic"
        
    response = client.post("/uploadAdvertisement", data = {
            "file": (resources / "re1.mp4").open("rb"),
            "caption": "DELETEME",


    }, follow_redirects = True)
    

    assert response.status_code == 200
    assert b"File uploaded successfully" in response.data
    assert response.request.path == '/uploadAdvertisement'



#ALTERNATE FLOW
#UC5-4
def test_delete_advertisement(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
    
    response = client.get("/deleteFile/9999", follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == '/dashboard'
    



#EXCEPTION FLOW
#UC5-5
def test_access_upload_page_unsubscribed(client):
    with client.session_transaction() as session:
        session["user_id"] = 18
        session["subscription_plan"] = "New"
    
    response = client.get("/uploadAdvertisement", follow_redirects=True)
    assert response.status_code == 200
    assert b"You are not subscribed to any plan. You must be subscribed to schedule an advertisement."
    assert response.request.path == '/dashboard'

#UC5-6
def test_upload_no_file_selected(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["subscription_plan"] = "Basic"
    
    response = client.post("/uploadAdvertisement", data = {
            "file": (io.BytesIO(b""), ""),
            "caption": "DELETEME",


    }, follow_redirects = True)

    assert response.status_code == 200
    assert b"No file selected" in response.data
    assert response.request.path == '/uploadAdvertisement'

#UC5-7
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

#UC5-8
def test_upload_existing_file(client):
    with client.session_transaction() as session:
        session["user_id"] = 3
        session["subscription_plan"] = "Basic"
    
    response = client.post("/uploadAdvertisement", data = {
            "file": (resources / "city_center.jpg").open("rb"),
            "caption": "DELETEME",


    }, follow_redirects = True)

    assert response.status_code == 200
    assert b"File already exists" in response.data
    assert response.request.path == '/uploadAdvertisement'

#UC5-9
def test_delete_file_not_owned(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
    
    response = client.get("/deleteFile/10049", follow_redirects=True)

    assert response.status_code == 200
    assert b"You are trying to delete a file that does not belong to you." in response.data
    assert response.request.path == '/dashboard'


    


#Used to wipe the testing details from the database
@pytest.fixture(scope="session", autouse=True)
def wipe_db():
    yield #Executes the function after all the tests are done

    resources = Path(__file__).parent.parent / "tests" / "resources" 
    backupResources = Path(__file__).parent.parent / "tests" / "backupresources" 

    #Used to copy the resources back in when they are deleted
    for file in backupResources.iterdir():
        destination = resources / file.name
        shutil.copy2(file,destination)

    database = MySQLdb.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DB"),
        port=int(os.getenv("MYSQL_PORT")),
        charset=os.getenv("MYSQL_CHARSET")
    )
    name = "DELETEME"
    cursor = database.cursor()
    cursor.execute("DELETE FROM advertisements WHERE caption = %s", (name,))
    cursor.execute("INSERT INTO advertisements (advert_id, file, caption, user_id, views) VALUES (%s,%s, %s, %s, %s)", (9999,"tests/resources/gp.mp4", "hi", 1, 33))
    cursor.connection.commit()

    cursor.close() 
    database.close()