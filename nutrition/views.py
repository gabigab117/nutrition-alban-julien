from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Plate, Ingredient, PlateIngredient
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .choices import DietType
from .forms import PlateForm, PlateIngredientFormset
from django.db import transaction
from django.views.decorators.http import require_POST


class PlatesListView(LoginRequiredMixin, ListView):
    model = Plate
    template_name = "nutrition/user_plates.html"
    context_object_name = "plates"
    paginate_by = 3
    
    def get_queryset(self):
        queryset = Plate.objects.filter(user=self.request.user)
        
        search = self.request.GET.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(ingredients__ingredient__name__icontains=search)
            ).distinct()
        
        return queryset
    
    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["nutrition/partials/plates_list.html"]
        return [self.template_name]


class PlateDetailView(LoginRequiredMixin, DetailView):
    model = Plate
    
    def get_queryset(self):
        return Plate.objects.filter(user=self.request.user)


# # detail version fbv
# def plate_detail_view(request, pk):
#     plate = Plate.objects.get(pk=pk, user=request.user)
#     return render(request, "nutrition/plate_detail.html", {"plate": plate})


class PlateCreateView(LoginRequiredMixin, CreateView):
    model = Plate
    fields = ["name"]
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PlateDeleteView(LoginRequiredMixin, DeleteView):
    model = Plate
    success_url = reverse_lazy("nutrition:user_plates")
    
    def get_queryset(self):
        return Plate.objects.filter(user=self.request.user)


@login_required
def update_plate(request, pk):
    plate = get_object_or_404(Plate, pk=pk, user=request.user)
    
    if request.method == "POST":
        plate_form = PlateForm(request.POST, instance=plate)
        formset = PlateIngredientFormset(request.POST, queryset=plate.ingredients.all())
        if plate_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                plate_form.save()
                formset.save()
            return redirect(plate)
    else:
        plate_form = PlateForm(instance=plate)
        formset = PlateIngredientFormset(queryset=plate.ingredients.all())
    
    return render(request, "nutrition/update_plate_form.html", {
        "formset": formset,
        "plate_form": plate_form,
        "diet_type_choices": DietType.choices,
        "plate": plate,
    })


@login_required
def search_ingredients(request):
    query = request.GET.get("q", "").strip()
    plate_id = request.GET.get("plate_id")
    
    selected_diet_types = request.GET.getlist("diet_type")
    
    if len(query) < 2 and not selected_diet_types:
        return render(request, "nutrition/partials/ingredient_search_results.html", {
            "ingredients": None,
            "plate_id": plate_id
        })
    
    ingredients = Ingredient.objects.all()
    
    if len(query) >= 2:
        ingredients = ingredients.filter(name__icontains=query)
    
    if selected_diet_types:
        ingredients = ingredients.filter(diet_type__in=selected_diet_types)
    
    ingredients_pk_to_exclude = PlateIngredient.objects.filter(plate_id=plate_id).values_list("ingredient_id", flat=True)
    ingredients = ingredients.exclude(id__in=ingredients_pk_to_exclude)
    
    return render(request, "nutrition/partials/ingredient_search_results.html", {
            "ingredients": ingredients,
            "plate_id": plate_id
        })


@login_required
@require_POST
def add_ingredient_to_plate(request, plate_id, ingredient_id):
    plate = get_object_or_404(Plate, pk=plate_id, user=request.user)
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    quantity = request.POST.get("quantity")
    
    if not PlateIngredient.objects.filter(plate=plate, ingredient=ingredient).exists():
        PlateIngredient.objects.create(
            plate=plate,
            ingredient=ingredient,
            quantity=int(quantity)
        )
    
    formset = PlateIngredientFormset(queryset=plate.ingredients.all())
    
    return render(request, "nutrition/partials/ingredients_formset.html",
                  {
                      "formset": formset,
                      # "plate": plate
                  })
    
