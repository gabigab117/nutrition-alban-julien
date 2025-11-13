from django.urls import path
from .views import signup_view, activate


app_name = "accounts"
urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
]
