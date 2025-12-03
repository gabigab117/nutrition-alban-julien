from django.urls import path
from .views import PlatesListView, PlateDetailView, PlateCreateView


app_name = "nutrition"
urlpatterns = [
    path("user-plates/", PlatesListView.as_view(), name="user_plates"),
    path("plate/<int:pk>/", PlateDetailView.as_view(), name="plate_detail"),
    path("create/", PlateCreateView.as_view(), name="plate_create"),
]
