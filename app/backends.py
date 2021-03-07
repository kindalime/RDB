"""CAS authentication backend"""
from django_cas_ng.backends import CASBackend
from django.contrib.auth.models import User
from django.conf import settings
from rdb.settings import get_secret
import requests
from requests.exceptions import HTTPError


class RDBCASBackend(CASBackend):
    def configure_user(self, user: User) -> User:
        """
        Configures a user after creation and returns the updated user.

        This method is called immediately after a new user is created,
        and can be used to perform custom setup actions.

        :param user: User object.

        :returns: [User] The user object with updates to is_staff, email, first_name, last_name fields.
        """
        url = "https://yalies.io/api/people"
        querystring = {"query": user.username}
        headers = {
            'Authorization': f"Bearer {get_secret('YALIES_API')}",
        }

        try:
            response = requests.post(url, headers=headers, json=querystring)
            response.raise_for_status()
            data = response.json()[0]
            
            email = data['email']
            first_name = data['first_name']
            last_name = data['last_name']
            org = data['organization']
            is_staff = False
            if org is not None:
                is_staff = True

            user.email = email
            user.first_name = first_name 
            user.last_name = last_name
            user.is_staff = is_staff
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

        return user