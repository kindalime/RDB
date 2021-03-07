from django.dispatch import receiver
from django_cas_ng.signals import cas_user_authenticated, cas_user_logout

@receiver(cas_user_authenticated)
def cas_user_authenticated_callback(sender, **kwargs):
    pass

@receiver(cas_user_logout)
def cas_user_logout_callback(sender, **kwargs):
    pass