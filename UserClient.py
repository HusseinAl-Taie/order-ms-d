from flask import session
import requests


class UserClient:

    @staticmethod
    def get_user(api_key):
        headers = {
            'Authorization': api_key
        }

        response = requests.request(method="GET", url='http://docker.for.mac.localhost:8100/api/user', headers=headers)
        if response.status_code == 401:
            return False

        user = response.json()
        return user