from django.shortcuts import render
from .models import Plate
from django.views.generic import ListView
from django.db.models import Q


class PlatesListView(ListView):
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
