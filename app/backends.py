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
        url = 'https://yalies.io/api/people'
        payload = {
            'filters': {
                'netid': user.username,
            }
        }
        headers = {
            'Authorization': 'Bearer ' + get_secret('YALIES_API'),
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()[0]

            user.email = data['email']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.is_staff = (data['organization'] is not None)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

        return user
