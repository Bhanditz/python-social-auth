import json

from social.backends.oauth import BaseOAuth2
from urllib import urlencode

class TrinityOauth2(BaseOAuth2):
    name = 'trinity'
    REDIRECT_STATE = False # ????
    AUTHORIZATION_URL = 'https://pass-staging.texasgateway.org/oauth/v2/auth'
    ACCESS_TOKEN_URL = 'https://pass-staging.texasgateway.org/oauth/v2/token'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    #DEFAULT_SCOPE = ['email']
    EXTRA_DATA = [
        ('email', 'email'),
        ('username', 'username'),
        ('fullname', 'fullname'),
        ('district', 'district'),
    ]

    def get_user_details(self, response):
        """Return user details from Trinity account"""
        fullname, first_name, last_name = self.get_user_names(
            '', response.get('first_name', ''),response.get('last_name', '')
        )
        data = {'username': response.get('username'),
                'email': response.get('email') or '',
                'fullname': fullname or '',
                'district': response.get('original_district')}
        return data

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://pass-staging.texasgateway.org/api/v1/user/me?' + urlencode({
            'access_token': access_token
        })
        return self.get_json(url)

    def get_user_id(self, details, response):
        """Use trinity username as unique id"""
        return details['email']
