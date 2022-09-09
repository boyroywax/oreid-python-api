import requests
import os


class OreIdApi:
    base_url: str = os.getenv("API_URL")
    headers: dict = {
        "api-key": os.getenv("OREID_API_KEY"),
        # "app_id": os.getenv("OREID_APP_ID"),
        # "service-key": os.getenv("OREID_SERVICE_KEY"),
        "content-type": "application/json",
    }

    def prepare_response(self, response: requests.Response) -> dict:
        print(f'status: {response.status_code} response: {response.json()}')
        return response.json()

    def make_call(self, *args, **kwargs) -> dict:
        """ Calls the ORE ID API

        * args variable is a list containing the API action method (POST, GET, etc..)
        * kwargs variable is a dict containing the API endpoint and the payload

        Returns the response of the API call as a dict.

        https://documenter.getpostman.com/view/7805568/SWE55yRe
        """
        action: str = args[0]

        match(action):
            case "POST":
                response: requests.Response = requests.request(
                    action,
                    url=f'{self.base_url}{kwargs["endpoint"]}',
                    headers=self.headers,
                    data=kwargs.get("data", {})
                )
                return self.prepare_response(response)
            case "GET":
                response: requests.Response = requests.request(
                    action,
                    url=f'{self.base_url}{kwargs["endpoint"]}',
                    headers=self.headers,
                    params=kwargs.get("params", {})
                )
                return self.prepare_response(response)
            case _:
                error: dict = {"error": f"Action [{action}] is not supported"}
                print(error)
                return error

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

    def new_user_with_token(self, id_token: str) -> dict:
        """Creates a new user on the ORE ID Service

        https://documenter.getpostman.com/view/7805568/SWE55yRe#9ad14572-b4dd-4c83-975b-46d2c5204734
        """
        args = ["POST"]
        kwargs = {
            "endpoint": "account/login-user-with-token",
            "data": {
                "id_token": id_token
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
