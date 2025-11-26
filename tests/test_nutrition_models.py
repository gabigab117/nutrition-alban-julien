import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from nutrition.models import Ingredient
from nutrition.choices import FoodType, DietType, QuantityUnit


@pytest.mark.django_db
def test_clean_validation_piece_without_weight():
    """
    Given an ingredient with unit PIECE but no average weight
    When validate the ingredient
    Then it raises a ValidationError
    """
    ingredient = Ingredient(
            name="test",
            food_type=FoodType.FRUIT,
            diet_type=DietType.VEGAN,
            default_unit=QuantityUnit.PIECE,
            average_piece_weight=0
        )
    with pytest.raises(ValidationError):
        ingredient.clean()


@pytest.mark.django_db
def test_unique_together_constraint():
    """
    Given two ingredients with the same name and food_type
    When trying to create the second one
    Then it raises an IntegrityError
    """
    Ingredient.objects.create(
        name="Pomme",
        food_type=FoodType.FRUIT,
        diet_type=DietType.VEGAN,
        default_unit=QuantityUnit.GRAM
    )
    
    with pytest.raises(IntegrityError):
        Ingredient.objects.create(
            name="Pomme",
            food_type=FoodType.FRUIT,
            diet_type=DietType.VEGETARIAN,
            default_unit=QuantityUnit.PIECE,
            average_piece_weight=150
        )



