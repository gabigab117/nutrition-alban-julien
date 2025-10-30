from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from utils.validators import LETTER_SPACE_DASH_VALIDATOR


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **kwargs):
        if not username:
            raise ValueError("L'username doit être renseigné")
        if not email:
            raise ValueError("L'email doit être renseigné")
        user = self.model(
            username=username, email=self.normalize_email(email), **kwargs
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        
        if kwargs.get("is_staff") is not True:
            raise ValueError("Le super user doit être staff")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Le super user doit être admin")
        
        return self.create_user(username, email, password, **kwargs)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, verbose_name="Prénom", validators=[LETTER_SPACE_DASH_VALIDATOR])
    last_name = models.CharField(max_length=150, verbose_name="Nom", validators=[LETTER_SPACE_DASH_VALIDATOR])
    
    objects = CustomUserManager()
