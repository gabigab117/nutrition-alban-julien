from django.urls import path
from .views import PlatesListView


app_name = "nutrition"
urlpatterns = [
    path("user-plates/", PlatesListView.as_view(), name="user_plates"),
]
