import os
from oauthlib.oauth2 import WebApplicationClient
import requests
from urllib.parse import urlparse, parse_qs
import json
import aiohttp
from aiohttp.helpers import BasicAuth


def googleOauth():

    # Configuration
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )

    def get_google_provider_cfg():
        return requests.get(GOOGLE_DISCOVERY_URL).json()

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    print(token_endpoint)

    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    print(f'authorization endpoint: {authorization_endpoint}')

    client = WebApplicationClient(GOOGLE_CLIENT_ID, code=GOOGLE_CLIENT_SECRET)
    # auth_request = client.prepare_authorization_request(authorization_endpoint)
    # print(auth_request[0])

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        # grant_type="refresh_token",
        scope=["openid", "email", "profile"],
        state="state"
    )
    print(f'request: {request_uri}')

    # authorize = requests.get(auth_request[0], headers=auth_request[1])
    authorize = requests.get(request_uri, headers={'Content-Type': 'application/x-www-form-urlencoded'}, auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET))
    print(authorize.text)

    # print(client.parse_request_uri_response(request_uri, state="state"))
    # client.parse_request_body_response(request_uri)

    # token_url, headers, body = client.prepare_token_request(
    #     token_endpoint
    # )
    token_url = "https://oauth2.googleapis.com/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'authorization_code', 'client_id': '331243472633-l1s9b4eip0ioatoihombl04v2pgle5kf.apps.googleusercontent.com', 'code': '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'}

    print(f'token url: {token_url}')
    print(f'headers: {headers}')
    token_response = client.prepare_refresh_token_request(token_url)
    # print(f'body: {parse_qs(urlparse(body).path)}')
    # body = parse_qs(urlparse(body).path)
    # body = client.(body)
    # data = {
    #         "grant_type": body["grant_type"][0],
    #         "client_id": body["client_id"][0],
    #         "code": body["code"][0],
    # }

    # print(data)
    # print(client.populate_token_attributes())
    # client.add_token(authorization_endpoint, data=data)
    # print("access_token: " + client.access_token)

    # token_response = requests.post(
    #     token_url,
    #     headers=headers,
    #     data=data,
    #     auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    # )
    # api.setHeaders(json.dumps(headers))
    # api.setBaseUrl(request_uri)
    # token_response = await api.makeCall('GET', None, token_url, body)

    # client.parse_request_body_response(token_response)
    print(token_response)
    return token_response
