from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .models import Lab

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
    labs = Lab.objects.filter(edit__contains=[request.user])
    return render(request, "profile.html", {'user': user, 'labs': labs})

class LabDetail(LoginRequiredMixin, DetailView):
    model = Lab
    fields = '__all__'

class LabCreate(LoginRequiredMixin, CreateView):
    model = Lab
    fields = '__all__'

    def form_valid(self, form, edit):
        self.object = form.save(commit=False)
        self.object.edit = edit
        self.object.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        edit = request.POST.get("netID").split(',')

        if request.user.username not in edit:
            edit.append(request.user.username)

        edit = list(set(list(filter(None, edit))))
        pi_netid_lab = Lab.objects.filter(pi_id=form['pi_id'].value())
        pi_netid_exists = pi_netid_lab.exists()

        pi_netid_lab = pi_netid_lab[0].name
        print(pi_netid_lab)
        
        if form.is_valid() and not pi_netid_exists:
            return self.form_valid(form, edit)
        elif pi_netid_exists:
            return render(request, 'app/lab_form.html', {'form': form, 'pi_netid_error': pi_netid_lab + " is already associated with " + form['pi_id'].value(), 'prev_pi_netid': form['pi_id'].value()})
        else:
            return self.form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class LabUpdate(LoginRequiredMixin, UpdateView):
    model = Lab
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        edit = request.POST.get("netID").split(',')

        if request.user.username not in edit:
            edit.append(request.user.username)
        
        edit = list(set(list(filter(None, edit))))

        self.object.edit = edit
        self.object.save()
        return super().post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.username not in self.get_object().edit:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class LabDelete(LoginRequiredMixin, DeleteView):
    model = Lab
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        if request.user.username not in self.get_object().edit:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)