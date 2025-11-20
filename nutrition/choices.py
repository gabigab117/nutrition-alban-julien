from django.db import models


class FoodType(models.TextChoices):
    PROTEIN = "PROT", "Protein"
    CARBOHYDRATE = "CARB", "Carbohydrate"
    VEGETABLE = "VEG", "Vegetable"
    FRUIT = "FRUIT", "Fruit"
    HEALTHY_FAT = "HFAT", "Healthy Fat"
    OTHER = "OTHER", "Other"


class DietType(models.TextChoices):
    OMNIVORE = "OMNI", "Omnivore"
    VEGETARIAN = "VEG", "Vegetarian"
    VEGAN = "VEGAN", "Vegan"


class QuantityUnit(models.TextChoices):
    GRAM = "G", "Gram"
    PIECE = "P", "Piece"
