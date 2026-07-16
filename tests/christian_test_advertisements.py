
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
        
    
    response = client.post("/uploadAdvertisement", data = {
            "file": (resources / "45aafe5bd2b9c215500567c0f1fa9804.jpg").open("rb"),
            "caption": "DELETEME"


    }, follow_redirects = True)

    assert response.status_code == 200
    assert b"File uploaded successfully" in response.data
    assert response.request.path == '/uploadAdvertisement'

#UC5-3
def test_upload_advertisement_video(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        
    
    response = client.post("/uploadAdvertisement", data = {
            "file": (resources / "a ghost pepper itself😃 [Ogc_pAgrZyM].mp4").open("rb"),
            "caption": "DELETEME"


    }, follow_redirects = True)

    assert response.status_code == 200
    assert b"File uploaded successfully" in response.data
    assert response.request.path == '/uploadAdvertisement'





#Used to wipe the testing details from the database
@pytest.fixture(scope="session", autouse=True)
def wipe_db():
    yield #Executes the function after all the tests are done
    database = MySQLdb.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DB"),
        port=int(os.getenv("MYSQL_PORT"))
    )
    cursor = database.cursor()
    cursor.execute("DELETE FROM advertisements WHERE caption = %s", ("DELETEME",))
    cursor.connection.commit()

    cursor.close() 
    database.close()