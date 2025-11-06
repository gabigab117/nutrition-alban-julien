import pytest
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="DBezjfhgdgefgeydfg123"
    )


@pytest.fixture
def user2():
    return User.objects.create_user(
        username="testuser2",
        email="test2@example.com",
        password="DBezjfhgdgefgeydfg123"
    )
    