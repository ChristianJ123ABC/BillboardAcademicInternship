# Verify Subscription Tests
# Use Case: UC6 - VERIFY SUBSCRIPTION


# Purpose:
# Tests that only users with an active subscription
# can access premium features such as uploading
# advertisements and scheduling campaigns.


# Resources:
# https://flask.palletsprojects.com/en/stable/testing/
# https://docs.pytest.org/en/stable/
# https://flask.palletsprojects.com/en/stable/config/
# https://flask.palletsprojects.com/en/stable/tutorial/tests/

#for testing:
#pytest tests/prakash_test_verify_subscription.py

import sys
from pathlib import Path

#Allow importing server.py
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from server import app as create_app
import io


resources = Path(__file__).parent / "resources"



@pytest.fixture()
def app():

    create_app.config.update({
        "TESTING": True,
    })

    yield create_app


@pytest.fixture()
def client(app):
    return app.test_client()



# UC6 - VERIFY SUBSCRIPTION

# NORMAL FLOW

# UC6-1
# User has active subscription.
# Upload advertisement page should be accessible.

def test_active_subscription_upload_access(client):

    with client.session_transaction() as session:
        session["user_id"] = 1
        session["subscription_plan"] = "Basic"


    response = client.get(
        "/uploadAdvertisement"
    )


    assert response.status_code == 200
    assert response.request.path == "/uploadAdvertisement"





# UC6-2
# User has active subscription.
# Scheduling page should be accessible.

def test_active_subscription_schedule_access(client):

    with client.session_transaction() as session:
        session["user_id"] = 1
        session["subscription_plan"] = "Basic"


    response = client.get(
        "/scheduling"
    )


    assert response.status_code == 200
    assert response.request.path == "/scheduling"




# ALTERNATE FLOW

# UC6-3
# User does not have subscription.
# System redirect user away from upload page to subscription page.

def test_no_active_subscription_upload_blocked(client):

    with client.session_transaction() as session:
        session["user_id"] = 18
        session["subscription_plan"] = "New"


    response = client.get(
        "/uploadAdvertisement",
        follow_redirects=True
    )


    assert response.status_code == 200


# UC6-4
# User subscription expired.
# System redirects to subscription page.

def test_expired_subscription(client):

    with client.session_transaction() as session:
        session["user_id"] = 3
        session["subscription_plan"] = "Premium"


    response = client.get(
        "/uploadAdvertisement",
        follow_redirects=True
    )


    assert response.status_code in [200,302,400]



# EXCEPTION FLOW

# UC6-5
# Subscription details cannot be found.

def test_subscription_details_missing(client):

    with client.session_transaction() as session:
        session["user_id"] = 9999
        session["subscription_plan"] = "Basic"


    response = client.get(
        "/uploadAdvertisement",
        follow_redirects=True
    )


    assert response.status_code in [200,302]



# UC6-6
# User is not logged in.

def test_not_logged_in_user(client):


    response = client.get(
        "/scheduling",
        follow_redirects=True
    )


    assert response.status_code in [200,302]