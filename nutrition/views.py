from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Plate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.db.models import Q


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
