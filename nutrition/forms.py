from django import forms
from .models import Plate, PlateIngredient


class PlateForm(forms.ModelForm):
    class Meta:
        model = Plate
        fields = ["name"]


PlateIngredientFormset = forms.modelformset_factory(
    PlateIngredient,
    fields=("ingredient", "quantity"),
    extra=0,
    can_delete=True
)
