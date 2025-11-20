import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


VALID_SIGNUP_DATA = {
    "username": "patrick117",
    "email": "p117@patrick.com",
    "first_name": "Patrick",
    "last_name": "Rondat",
    "password1": "Mot_de_Passe123",
    "password2": "Mot_de_Passe123",
}


@pytest.mark.django_db
def test_signup_view(mailoutbox, client: Client):
    """
    Given a user with valid data
    When submit the signup form
    Then a new inactive user and activation mail should be sent
    """
    response = client.post(reverse("accounts:signup"), data=VALID_SIGNUP_DATA)
    
    user = User.objects.get(email=VALID_SIGNUP_DATA["email"])
    assert response.status_code == 302
    assert len(mailoutbox) == 1
    assert user.is_active is False


@pytest.mark.django_db
def test_successful_account_activation(mailoutbox, client: Client):
    """
    Given an inactive user who just signed up
    When the user clicks on the activation link
    Then the user account should be activated
    """
    # Sign up the user
    client.post(reverse("accounts:signup"), data=VALID_SIGNUP_DATA)
    user = User.objects.get(email=VALID_SIGNUP_DATA["email"])
    
    # Extract activation link from email
    email_body = mailoutbox[0].body
    activation_link = [line for line in email_body.splitlines() if "/activate/" in line][0]
    
    # Simulate clicking the activation link
    client.get(activation_link)
    
    user.refresh_from_db()
    assert user.is_active is True
