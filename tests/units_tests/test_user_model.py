import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError


User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    """
    Given valid user data
    When creating a user
    Then the user should be created with correct attributes and not be a staff or superuser
    """
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="motdepasse12343444"
    )
    assert user.username == "testuser"
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_create_superuser():
    superuser = User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="motdepasse2214244242"
    )
    assert superuser.is_staff
    assert superuser.is_superuser


@pytest.mark.django_db
def test_create_user_without_username():
    """
    ...
    """
    with pytest.raises(ValueError, match="L'username doit être renseigné"):
        User.objects.create_user(
            username="",
            email="test@test.com",
            password="Testfefeg124424242424"
        )


@pytest.mark.django_db
def test_email_unique(user2):
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            username="AlbanJulien",
            email="test2@example.com",
            password="DBezjfhgdgefgeydfg123"
        )
