from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from .models import Lab
import json

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def search(request):
    search_term = request.GET.get('q', None)
    if not search_term:
        raise Http404('Send a search term')

    labs = Lab.objects.search(search_term)

    response_data = [
        {
            'rank': lab.rank,
            'name': lab.name,
            'description': lab.project_desc,
            'url': lab.get_absolute_url(),
        } for lab in labs
    ]

    return render(request, 'search.html', {'response_data': response_data})

def lucky(request):
    return render(request, 'search.html', {'response_data':  [Lab.objects.order_by('?').first(), ]})


class LabDetail(LoginRequiredMixin, DetailView):
    model = Lab
    fields = '__all__'

class LabCreate(LoginRequiredMixin, CreateView):
    model = Lab
    fields = '__all__'

class LabUpdate(LoginRequiredMixin, UpdateView):
    model = Lab
    fields = '__all__'

class LabDelete(LoginRequiredMixin, DeleteView):
    model = Lab
    success_url = "/"
    # success_url = reverse_lazy('Lab')