from dis import disco
import json
import os
import urllib.parse
import requests

from modules.call_api import Api


class GoogleOauth():
    """Make Api calls to Google's Oauth service.

    * Includes functions to verify the info received.

    https://cloud.google.com/identity-platform/docs/web/oidc
    """
    headers: dict = {'Content-Type': 'application/json'}
    client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET")
    client_id: str = os.getenv("GOOGLE_CLIENT_ID")
    discovery_url: str = "https://accounts.google.com/.well-known/openid-configuration"
    scope: str = "openid email profile"
    redirect_uri: str = os.getenv("GOOGLE_REDIRECT_URI")
    auth_uri: str = 'https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={}&redirect_uri={}&scope={}'.format(client_id, redirect_uri, scope)
    token_endpoint: str = "https://oauth2.googleapis.com/token"
    authorization_endpoint: str = 'https://accounts.google.com/o/oauth2/v2/auth'
    authorization_endpoint_params: dict = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope
    }
    auth_uri_encoded = authorization_endpoint + "?" + urllib.parse.urlencode(
            authorization_endpoint_params
        )
    request_uri: str = None
    state: str = "Testing"
    api_instance: Api = Api(headers=headers)
    make_call = api_instance.make_call

    def get_discovery(self) -> dict:
        """Retrieve info using Google's Discover Url
        
        """
        args = ["GET"]
        kwargs = {
            "url": self.discovery_url
        }
        return self.make_call(*args, **kwargs)

    def verify_discovery(self, discover: dict) -> dict:
        """ Check the discovery result and update self.

        """
        if discover.get("exception", None) is None:
            try:
                self.authorization_endpoint = discover["response"].get(
                    "authorization_endpoint", self.authorization_endpoint
                )
                self.token_endpoint = discover["response"].get(
                    "token_endpoint", self.token_endpoint
                )
                discover["verified"] = True
            except Exception as exc:
                discover["verified"] = False
                discover["discover_exception"] = exc.with_traceback.__repr__
        else:
            discover["verified"] = False
        return discover

    def get_token(self, code: str) -> dict:
        """Retrieve info using Google's Discover Url
        
        """
        args = ["POST"]
        kwargs = {
            "url": self.token_endpoint,
            "params": {
                'grant_type': 'authorization_code',
                'redirect_uri': self.redirect_uri,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': code,
            }
        }
        return self.make_call(*args, **kwargs)

    def verify_token(self, token: dict) -> dict:
        """Check the token result and return token

        """
        if token.get("exception", None) is None:
            token["verified"] = True
            try:
                if token["response"].get("id_token", None) is not None:
                    token["verified"] = True
                else:
                    token["verified"] = False
            except Exception as exc:
                token["verified"] = False
                token["verify_exception"] = exc.with_traceback.__repr__
        else:
            token["verified"] = False
        return token
