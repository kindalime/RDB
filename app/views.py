from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .models import Lab
from django.http import JsonResponse
import json

def index(request):
    labs = Lab.objects.all()
    return render(request, "construction.html", {'labs': labs})

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def search(request):
    query = request.GET.get("q", None)
    if not query:
        return HttpResponseRedirect("/")

    labs = Lab.objects.search(query)

    return render(request, 'construction.html', {'labs': labs})

def random(request):
    return HttpResponseRedirect(Lab.objects.order_by('?').first().get_absolute_url())

def profile(request):
    user = User.objects.get(username=request.user)
    return render(request, "construction.html", {'user': user})

class LabDetail(LoginRequiredMixin, DetailView):
    model = Lab
    fields = '__all__'

class LabCreate(LoginRequiredMixin, CreateView):
    model = Lab
    fields = '__all__'

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.pi_id = str(self.request.user)
    #     self.object.save()
    #     return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class LabUpdate(LoginRequiredMixin, UpdateView):
    model = Lab
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class LabDelete(LoginRequiredMixin, DeleteView):
    model = Lab
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)