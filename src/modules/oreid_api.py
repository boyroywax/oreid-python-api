import os

from modules.call_api import Api


class OreIdApi:
    """  Make Api calls to the ORE ID Api.

    """
    base_url: str = os.getenv("OREID_API_URL")
    headers: dict = {
        "api-key": os.getenv("OREID_API_KEY"),
        # "app_id": os.getenv("OREID_APP_ID"),
        "service-key": os.getenv("OREID_SERVICE_KEY"),
        "content-type": "application/json",
    }
    api_instance: Api = Api(base_url=base_url, headers=headers)
    make_call = api_instance.make_call

    def raw_action(self, args: list, kwargs: dict) -> dict:
        return self.make_call(*args, **kwargs)

    def get_access_token(self, data: dict = {}) -> dict:
        """Retrive an ORE ID Service App Access Token
        
        https://documenter.getpostman.com/view/7805568/SWE55yRe#130ffe5d-0832-488a-a2a0-e46b3e02399d
        """
        args = ["POST"]
        kwargs = {
            "endpoint": "app-token",
        }
        if data.get("newAccountPassword", None) is not None:
            kwargs["data"] = {
                "newAccountPassword": data["newAccountPassword"]
            }
        return self.make_call(*args, **kwargs)

    def get_chains(self, chainNetwork: str = None) -> dict:
        """Retrieve the supported chain/s info
        
        https://documenter.getpostman.com/view/7805568/SWE55yRe#9e17c8c9-22cf-4ebc-bfba-fbc2ee486ba8
        """
        args = ["GET"]
        kwargs = {
            "endpoint": "services/config",
            "params": {
                "type": "chains"
            }
        }
        if chainNetwork is not None:
            kwargs["params"] = {
                "type": "chain",
                "chainNetwork": chainNetwork
            }
        return self.make_call(*args, **kwargs)

    def get_user(self, account_name: str) -> dict:
        """Retreive a user from the ORE ID Service

        https://documenter.getpostman.com/view/7805568/SWE55yRe#0dcb20f5-7a71-4307-bc5f-4ccab9e5b1c5
        """
        args = ["GET"]
        kwargs = {
            "endpoint": "account/user",
            "params": {
                "account": account_name
            }
        }
        return self.make_call(*args, **kwargs)

    def login_user_with_token(self, id_token: str, provider: str) -> dict:
        """Creates a new user on the ORE ID Service

        https://documenter.getpostman.com/view/7805568/SWE55yRe#9ad14572-b4dd-4c83-975b-46d2c5204734
        """
        args = ["POST"]
        kwargs = {
            "endpoint": "account/login-user-with-token",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "data": {
                "id_token": id_token,
                "provider": provider
            }
        }
        return self.make_call(*args, **kwargs)

    def new_custodial_account(self, data: dict) -> dict:
        """Create a new custodial user

        https://documenter.getpostman.com/view/7805568/SWE55yRe#c3709139-724f-482a-92e4-0f6b66b4cdb2
        """
        args = ["POST"]
        kwargs = {
            "endpoint": "custodial/new-user",
            "data": data
        }
        return self.make_call(*args, **kwargs)

    def new_chain_account(self, body: dict) -> dict:
        """Create a blockchain account for a cutodial ORE ID User

        https://documenter.getpostman.com/view/7805568/SWE55yRe#351535f4-a5ce-4600-a738-e9667d907044
        """
        args = ["POST"]
        kwargs = {
            "endpoint": "custodial/new-chain-account",
            "data": body
        }
        return self.make_call(*args, **kwargs)

    def verify_login(self, login_response: dict) -> dict:
        """Check the login result and return the result
        """
        if login_response.get("exception", None) is None:
            if login_response["response"].get("account", None) is not None:
                login_response["verified"] = True
        else:
            login_response["verified"] = False
        return login_response
