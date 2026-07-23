# Manage Subscription Tests

# Use Case: UC-5 Manage Subscriptions

# Purpose:
# Tests subscription page access and subscription
# management behaviour.

# Resources:
# https://flask.palletsprojects.com/en/stable/testing/
# https://docs.pytest.org/en/stable/
# https://flask.palletsprojects.com/en/stable/config/
# https://flask.palletsprojects.com/en/stable/tutorial/tests/
# https://docs.stripe.com/payments/checkout/how-checkout-works
# https://docs.stripe.com/payments/checkout/build-subscriptions

# pytest tests/prakash_test_manage_subscription.py


import sys
from pathlib import Path

#Allow importing server.py
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from server import app as create_app


@pytest.fixture()
def app():

    create_app.config.update({
        "TESTING": True,
    })


    yield create_app


@pytest.fixture()
def client(app):

    return app.test_client()


# UC5 - MANAGE SUBSCRIPTIONS
# NORMAL FLOW

# UC5-1
# Logged-in user opens subscription page.
# System displays available plans.

def test_access_subscription_page(client):


    with client.session_transaction() as session:

        session["user_id"] = 1



    response = client.get(
        "/subscription"
    )


    assert response.status_code == 200
    assert response.request.path == "/subscription"


# UC5-2
# User selects subscription plan.
# System redirects to Stripe checkout.

def test_choose_subscription_plan(client):

    with client.session_transaction() as session:
        session["user_id"] = 1

    response = client.get(
        "/create-checkout-session/Basic",
        follow_redirects=False
    )

    assert response.status_code == 303



# ALTERNATE FLOW

# UC5-3
# User cancels payment.
# System returns user to subscription page.

def test_cancel_payment(client):


    with client.session_transaction() as session:

        session["user_id"] = 1



    response = client.get(
        "/subscription",
        follow_redirects=True
    )


    assert response.status_code == 200
    assert response.request.path == "/subscription"



# EXCEPTION FLOW


# UC5-4
# User selects an invalid subscription plan.
# System displays an error.

def test_invalid_subscription_plan(client):

    with client.session_transaction() as session:
        session["user_id"] = 1

    response = client.get(
        "/choose-plan/Gold",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Invalid subscription plan" in response.data



# UC5-5
# User is not logged in.
# System redirects user to login page.

def test_subscription_without_login(client):

    response = client.get(
        "/subscription",
        follow_redirects=False
    )

    assert response.status_code == 302