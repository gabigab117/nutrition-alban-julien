from django.urls import path
from .views import PlatesListView, PlateDetailView, PlateCreateView, PlateDeleteView, \
    update_plate, search_ingredients, add_ingredient_to_plate


app_name = "nutrition"
urlpatterns = [
    path("user-plates/", PlatesListView.as_view(), name="user_plates"),
    path("plate/<int:pk>/", PlateDetailView.as_view(), name="plate_detail"),
    path("create/", PlateCreateView.as_view(), name="plate_create"),
    path("delete/<int:pk>/", PlateDeleteView.as_view(), name="plate_delete"),
    path("plate/<int:pk>/update/", update_plate, name="update_plate"),
    path("search-ingredients/", search_ingredients, name="search_ingredients"),
    path("plate/<int:plate_id>/add-ingredient/<int:ingredient_id>/", add_ingredient_to_plate, name="add_ingredient")
]
