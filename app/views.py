from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from app.serializers import LabSerializer
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Lab
from habanero import cn
from rdb.settings import DEBUG
import json

def index(request):
    labs = Lab.objects.all()
    return render(request, "index.html", {'labs': labs, 'labs_length': len(labs)})

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def dashboard(request):
    labs = Lab.objects.all()
    return render(request, "student_view.html", {'labs': labs, 'labs_length': len(labs)})

def search(request):
    query = request.GET.get("q", None)
    if not query:
        return HttpResponseRedirect("/")
    labs = Lab.objects.search(query)
    return render(request, "search.html", {'labs': len(labs)})

def like(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        slug = request.POST['slug']
        lab = get_object_or_404(Lab, slug=slug)
        liked = user in lab.likes.all()
        if liked:
            lab.likes.remove(user)
        else:
            lab.likes.add(user)
    return JsonResponse({'liked':liked, 'lab':lab.name})

def labs_json(request):
    hipaa_fields = [lab.name for lab in Lab._meta.get_fields()]
    hipaa_fields.remove('id')
    hipaa_fields.remove('pi_id')
    hipaa_fields.remove('search_vector')
    hipaa_fields.remove('edit')
    hipaa_fields.remove('publications')
    queryset = Lab.objects.all().values(*hipaa_fields)
    
    serializer = LabSerializer(Lab.objects.all(), many=True)

    # return JsonResponse({"data": list(queryset)})
    return JsonResponse({"data": serializer.data})

def search(request):
    query = request.GET.get("q", None)
    if not query:
        return HttpResponseRedirect("/")
    labs = Lab.objects.search(query)
    return render(request, "search.html", {'labs': len(labs)})

def random(request):
    return HttpResponseRedirect(Lab.objects.order_by('?').first().get_absolute_url())

def staff(request):
    if not request.user.is_superuser:
        return self.handle_no_permission()
    
    try:
        netid = request.GET.get("netid", None)
        user = User.objects.get(username=netid)
        user.is_staff = True
        user.save()
        
        user = User.objects.get(username=request.user)
        labs = Lab.objects.filter(edit__contains=[request.user])
        all_labs = Lab.objects.all()
        liked_labs = labs
        return render(request, "profile.html", {'user': user, 'labs': labs, 
                                                'all_labs': all_labs, 'liked_labs': liked_labs,
                                                'faculty_message': netid + ' has been successfully added as faculty.'})
    except:
        user = User.objects.get(username=request.user)
        labs = Lab.objects.filter(edit__contains=[request.user])
        all_labs = Lab.objects.all()
        liked_labs = labs
        return render(request, "profile.html", {'user': user, 'labs': labs, 
                                                'all_labs': all_labs, 'liked_labs': liked_labs,
                                                'faculty_message': netid + ' has caused an error.'})
        
def profile(request):
    user = User.objects.get(username=request.user)
    labs = Lab.objects.filter(edit__contains=[request.user])
    liked_labs = Lab.objects.filter(likes__in=[request.user])
    all_labs = Lab.objects.all()
    return render(request, "profile.html", {'user': user, 'labs': labs, 'all_labs': all_labs, 'liked_labs': liked_labs})

def email(request):
    user = User.objects.get(username=request.user)
    subject = 'Lab Created Successfully'
    message = '''RDB has received your lab submission. Please retain this email for your records.\n
    \n
    Kind regards,\n
    The RDB Team'''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email,]
    send_mail(subject, message, email_from, recipient_list)
    return

class LabDetail(LoginRequiredMixin, DetailView):
    model = Lab
    fields = '__all__'

class LabCreate(LoginRequiredMixin, CreateView):
    model = Lab
    fields = '__all__'
    
    def form_valid(self, form, edit, publications):
        self.object = form.save(commit=False)
        self.object.edit = edit
        self.object.publications = publications
        self.object.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        edit = request.POST.get("netID").split(',')
        publications = [self.detectDOI(v) for k, v in request.POST.items() if k.startswith('pubList_')]

        if request.user.username not in edit:
            edit.append(request.user.username)

        edit = list(set(list(filter(None, edit))))
        pi_netid_lab = Lab.objects.filter(pi_id=form['pi_id'].value())
        pi_netid_exists = pi_netid_lab.exists()
        if pi_netid_exists:
            pi_netid_lab = pi_netid_lab[0].name
        
        if form.is_valid() and not pi_netid_exists:
            # email(request)
            return self.form_valid(form, edit, publications)
        elif pi_netid_exists:
            return render(request, 'app/lab_form.html', {'form': form, 'pi_netid_error': "'" + pi_netid_lab + "'" + " is already associated with " + form['pi_id'].value() + ".", 'prev_pi_netid': form['pi_id'].value()})
        else:
            return self.form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if DEBUG:
            if not request.user.is_authenticated:
                return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)
        else:
            if not request.user.is_staff:
                return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)
    
    def detectDOI(self, DOI):
        try:
            APA = str(cn.content_negotiation(ids = DOI, format = "text", style = "apa")).strip("', /\n")
        except:
            APA = DOI
        return APA

class LabUpdate(LoginRequiredMixin, UpdateView):
    model = Lab
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        edit = request.POST.get("netID").split(',')
        if request.user.username not in edit and not request.user.is_superuser:
            edit.append(request.user.username)
        edit = list(set(list(filter(None, edit))))

        publications = [self.detectDOI(v) for k, v in request.POST.items() if k.startswith('pubList_')]

        self.object.edit = edit
        self.object.publications = publications
        self.object.save()
        return super().post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.username not in self.get_object().edit and not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def detectDOI(self, DOI):
        try:
            APA = str(cn.content_negotiation(ids = DOI, format = "text", style = "apa")).strip("', /\n")
        except:
            APA = DOI
        return APA

class LabDelete(LoginRequiredMixin, DeleteView):
    model = Lab
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        if request.user.username not in self.get_object().edit:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)