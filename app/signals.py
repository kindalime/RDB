import json

from django.dispatch import receiver
from django_cas_ng.signals import cas_user_authenticated, cas_user_logout

from django.contrib.auth.models import User
import requests

@receiver(cas_user_authenticated)
def cas_user_authenticated_callback(sender, **kwargs):
    '''
    This functions calls every time cas_user_authenticated finishes
    This callback fetches data from yalies API using the netid from cas
    and updates is_staff, email, first_name, last_name fields in the database
    '''
    args = {}
    args.update(kwargs)
    netid = args.get('user')

    key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTQ5NzY3OTAsInN1YiI6ImRsOTMzIn0.210dUOjuWZvvPrPGsOA7KqGOJTiR-9kZOS7_Fk2cf9c'
    url = "https://yalies.io/api/people"
    querystring = {"query": netid}
    headers = {
        'Authorization': f"Bearer {key}",
        }

    response = requests.post(url, headers = headers, json=querystring)
    if response.status_code==200:
        data = json.loads(response.text)[0]
        org = data['organization']
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']
        is_staff = False
        if org is not None:
            is_staff = True
    
    user = User.objects.get(username=netid)
    user.is_staff = is_staff
    user.email = email
    user.first_name = first_name 
    user.last_name = last_name
    user.save()
    


@receiver(cas_user_logout)
def cas_user_logout_callback(sender, **kwargs):
    pass
    # args = {}
    # args.update(kwargs)
    # print('''cas_user_logout_callback:
    # user: %s
    # session: %s
    # ticket: %s
    # ''' % (
    #     args.get('user'),
    #     args.get('session'),
    #     args.get('ticket')))