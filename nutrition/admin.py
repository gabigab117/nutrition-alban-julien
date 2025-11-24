from django.contrib import admin
from .models import Ingredient, Plate, PlateIngredient


class PlateIngredientInline(admin.TabularInline):
    model = PlateIngredient
    extra = 0


@admin.register(Ingredient)
class AdminIngredient(admin.ModelAdmin):
    list_display = ("name", "food_type", "calories_per_100g")
    search_fields = ("name", )
    list_filter = ("food_type", "diet_type")
    # list_editable = ("food_type", )


@admin.register(Plate)
class AdminPlate(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name", "user__email")
    inlines = [PlateIngredientInline]
