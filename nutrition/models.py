from django.db import models
from django.contrib.auth import get_user_model
from .choices import FoodType, DietType, QuantityUnit
from utils.validators import LETTER_SPACE_DASH_VALIDATOR


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=100, validators=[LETTER_SPACE_DASH_VALIDATOR], verbose_name="Nom")
    food_type = models.CharField(max_length=5, choices=FoodType, verbose_name="Type d'aliment")
    diet_type = models.CharField(max_length=5, choices=DietType, verbose_name="Type de régime")
    default_unit = models.CharField(max_length=2, choices=QuantityUnit, verbose_name="Unité par défaut")
    
    protein_per_100g = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Protéines pour 100g", default=0)
    carbs_per_100g = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Glucides pour 100g", default=0)
    fats_per_100g = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Lipides pour 100g", default=0)
    
    average_piece_weight = models.IntegerField(verbose_name="Poids moyen par pièce (g)", default=0)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    
    class Meta:
        verbose_name = "Ingrédient"
        ordering = ['name']
        unique_together = ('name', 'food_type')
    
    def __str__(self):
        return self.name


class Plate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur", related_name="plates")
    name = models.CharField(max_length=100, verbose_name="Nom du plat")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    
    class Meta:
        verbose_name = "Plat"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"


class PlateIngredient(models.Model):
    plate = models.ForeignKey(Plate, on_delete=models.CASCADE, verbose_name="Plat", related_name="ingredients")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Ingrédient")
    quantity = models.PositiveIntegerField(verbose_name="Quantité")
    
    class Meta:
        verbose_name = "Ingrédient du plat"
        verbose_name_plural = "Ingrédients du plat"
        unique_together = ('plate', 'ingredient')
    
    def __str__(self):
        return f"{self.quantity} x {self.ingredient.name} in {self.plate.name}"