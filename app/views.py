from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Lab

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

class LabCreate(CreateView):
    model = Lab
    fields = '__all__'

class LabUpdate(UpdateView):
    model = Lab
    fields = '__all__'

class LabDelete(DeleteView):
    model = Lab
    success_url = reverse_lazy('labs')