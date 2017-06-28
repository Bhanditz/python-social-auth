from social.backends.oauth import BaseOAuth2
from urllib import urlencode

class TrinityOauth2(BaseOAuth2):
    name = 'trinity'
    REDIRECT_STATE = False # ????
    AUTHORIZATION_URL = 'https://master-7rqtwti-yv37y7tzqm5f4.us.platform.sh/oauth/v2/auth'
    ACCESS_TOKEN_URL = 'https://master-7rqtwti-yv37y7tzqm5f4.us.platform.sh/oauth/v2/token'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    #DEFAULT_SCOPE = ['email']
    EXTRA_DATA = [
        ('email', 'email'),
        ('username', 'username'),
        ('full_name', 'full_name'),
    ]

    def get_user_details(self, response):
        """Return user details from GitHub account"""
        fullname, first_name, last_name = self.get_user_names(
            '', response.get('first_name', ''),response.get('last_name', '')
        )
        data = {'username': response.get('username'),
                'email': response.get('email') or '',
                'full_name': fullname or ''}
        return data

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://master-7rqtwti-yv37y7tzqm5f4.us.platform.sh/api/v1/user/me?' + urlencode({
            'access_token': access_token
        })
        return self.get_json(url)

    def get_user_id(self, details, response):
        """Use isc username as unique id"""
        return details['username']

    def oauth_authorization_request(self, token):
        """Generate OAuth request to authorize token."""
        if not isinstance(token, dict):
            token = parse_qs(token)
        params = self.auth_extra_arguments() or {}
        params.update(self.get_scope_argument())
        params[self.OAUTH_TOKEN_PARAMETER_NAME] = token.get(
            self.OAUTH_TOKEN_PARAMETER_NAME
        )
        state = self.get_or_create_state()
        params[self.REDIRECT_URI_PARAMETER_NAME] = self.get_redirect_uri(state)
        return '{0}?{1}'.format(self.authorization_url(), urlencode(params))
