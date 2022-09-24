import json
import os
from quart import Quart, redirect, request, url_for, render_template_string, session
from quart_auth import AuthUser, current_user, AuthManager, login_required, login_user, logout_user
import urllib.parse
from dotenv import load_dotenv

from modules.oreid_api import OreIdApi
from modules.google_oauth import GoogleOauth

# Initiate Modules and load env variables
load_dotenv()
google_oauth = GoogleOauth()
oreid_api = OreIdApi()

# Quart app setup
app = Quart(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
app.debug = True

# link authManager
auth_manager = AuthManager()
auth_manager.init_app(app)


@app.route("/")
async def index():
    return await render_template_string(
        f"Current User is Authenticated? {await current_user.is_authenticated}"
    )


@app.route("/oauth2callback")
async def oauth2callback():
    print(f"request args: {request.args.get('code', None)}")
    if 'code' not in request.args:
        if not await current_user.is_authenticated():
            return redirect(google_oauth.auth_uri_encoded)
        elif await current_user.is_authenticated():
            return redirect(url_for('user'))
    else:
        discovery: dict = google_oauth.get_discovery()
        verified_discover: dict = google_oauth.verify_discovery(discovery)
        print(verified_discover)
        discover_result: bool = verified_discover.get("verified", False)

    if discover_result is True:
        token: dict = google_oauth.get_token(request.args.get('code'))
        verified_token: dict = google_oauth.verify_token(token)
        print(verified_token)
        token_result = verified_token.get("verified", False)
    else:
        token_result = False

    if token_result is True:
        id_token: str = verified_token["response"].get("id_token", None)
        oreid_login_result = oreid_api.login_user_with_token(id_token, "google")
        verified_login: dict = oreid_api.verify_login(oreid_login_result)
        print(verified_login)
        login_result = verified_login.get("verified", False)
    else:
        login_result = False

    if login_result is True:
        # If successful log user into Quart Auth
        login_user(AuthUser(request.args.get('authuser', None)))
        session['token'] = verified_token.get('access_token', None)

        user_data = oreid_api.get_user(verified_login.get("account", None))
        print(f'user_data: {user_data}')
        return redirect(url_for('user'))
    else:
        return await render_template_string("Could not login")


@app.route("/login")
async def login():
    return redirect(google_oauth.auth_uri_encoded)


@login_required
@app.route("/user")
async def user():
    if await current_user.is_authenticated:
        return await render_template_string(
            # f"You have reached the User's Page.\n"
            f"Is user authenticated? {await current_user.is_authenticated()}"
        )
    else:
        return redirect(url_for('index'))


@login_required
@app.route("/logout")
async def logout():

    if session['token'] is not None:
        google_oauth.logout(session['token'])
        # print(f'logout_return: {logout_return}')
        logout_user()
    return redirect(url_for('index'))
