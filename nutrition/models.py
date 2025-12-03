from decimal import Decimal
from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from .choices import FoodType, DietType, QuantityUnit
from utils.validators import LETTER_SPACE_DASH_VALIDATOR
from django.core.exceptions import ValidationError


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=100, validators=[LETTER_SPACE_DASH_VALIDATOR], verbose_name="Nom")
    food_type = models.CharField(max_length=5, choices=FoodType, verbose_name="Type d'aliment")
    diet_type = models.CharField(max_length=5, choices=DietType, verbose_name="Type de régime")
    default_unit = models.CharField(max_length=2, choices=QuantityUnit, verbose_name="Unité par défaut")
    
    protein_per_100g = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Protéines pour 100g", default=0)
    carbs_per_100g = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Glucides pour 100g", default=0)
    fats_per_100g = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Lipides pour 100g", default=0)
    
    average_piece_weight = models.IntegerField(verbose_name="Poids moyen par pièce (g)", default=0) # blank=True, null=True, default=None
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    
    class Meta:
        verbose_name = "Ingrédient"
        ordering = ['name']
        unique_together = ('name', 'food_type')
        # constraints = [
        #     models.UniqueConstraint(fields=['name', 'food_type'], name='unique_ingredient_name_food_type')
        # ]
    
    def __str__(self):
        return self.name
    
    @property
    def calories_per_100g(self):
        result = self.protein_per_100g * 4 + self.carbs_per_100g * 4 + self.fats_per_100g * 9
        return result.quantize(Decimal("0.01"))
    
    def clean(self):
        super().clean()
        if self.default_unit == QuantityUnit.PIECE and self.average_piece_weight <= 0:
            raise ValidationError({"average_piece_weight": "Le poids moyen par pièce doit être positif"})


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
    
    def nutritional_profile(self):
        plate_ingredients = self.ingredients.select_related("ingredient").all()
        total_protein = 0
        total_carbs = 0
        total_fats = 0
        total_calories = 0
        
        for plate_ingredient in plate_ingredients:
            nutritional_values = plate_ingredient.get_nutritional_values()
            total_protein += nutritional_values["protein"]
            total_carbs += nutritional_values["carbs"]
            total_fats += nutritional_values["fats"]
            total_calories += nutritional_values["calories"]
        
        return {
            "total_protein": total_protein,
            "total_carbs": total_carbs,
            "total_fats": total_fats,
            "total_calories": total_calories
        }
    
    def get_absolute_url(self):
        return reverse("nutrition:plate_detail", kwargs={"pk": self.pk})


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
    
    def get_nutritional_values(self):
        quantity_in_grams = self._convert_to_grams()
        
        protein_per_gram = self.ingredient.protein_per_100g / 100
        carbs_per_gram = self.ingredient.carbs_per_100g / 100
        fats_per_gram = self.ingredient.fats_per_100g / 100
        calories_per_gram = self.ingredient.calories_per_100g / 100
        
        return {
            "protein": protein_per_gram * quantity_in_grams,
            "carbs": carbs_per_gram * quantity_in_grams,
            "fats": fats_per_gram * quantity_in_grams,
            "calories": calories_per_gram * quantity_in_grams,
        }
    
    def _convert_to_grams(self):
        if self.ingredient.default_unit == QuantityUnit.GRAM:
            return self.quantity
        else:
            return self.quantity * self.ingredient.average_piece_weight
    
    def display_unit(self):
        if self.ingredient.default_unit == QuantityUnit.GRAM:
            return "g"
        elif self.ingredient.default_unit == QuantityUnit.PIECE:
            return "p"