from typing import Any
import requests


class Api:
    base_url: str = "enter.an.api.url"
    headers: dict = None

    def __init__(
        self,
        url: str = None,
        base_url: str = None,
        headers: dict = None
    ) -> None:
        self.url = url
        self.base_url = base_url
        self.headers = headers

    def prepare_response(self, response: requests.Response) -> dict:
        try:
            output = {
                "status": response.status_code,
                "response": response.json()
            }
        except Exception as exc:
            output = {
                "status": response.status_code,
                "response": response.text,
                "exception": exc
            }
        return output

    def make_call(self, *args, **kwargs) -> dict:
        """ Calls an Api endpoint and returns the result.

        * args variable is a list containing the API action method (POST, GET, etc..)
        * kwargs variable is a dict containing the API endpoint and the payload

        Returns the response of the API call as Json.
        """
        action: str = args[0]
        if kwargs.get("url", None) is not None:
            self.url = kwargs.get("url")
        elif kwargs.get("endpoint", None) is not None:
            self.url = f'{self.base_url}{kwargs.get("endpoint")}'
        elif (kwargs.get("base_url", None) is not None) and (kwargs.get("endpoint", None) is not None):
            self.url = f'{kwargs.get("url")}{kwargs.get("endpoint")}'
        
        if kwargs.get("headers", None) is not None:
            self.headers = kwargs.get("headers")

        match(action):
            case "POST":
                response: requests.Response = requests.request(
                    action,
                    url=self.url,
                    headers=self.headers,
                    data=kwargs.get("data", None),
                    params=kwargs.get("params", None)
                )
                return self.prepare_response(response)
            case "GET":
                response: requests.Response = requests.request(
                    action,
                    url=self.url,
                    headers=self.headers,
                    params=kwargs.get("params", None)
                )
                return self.prepare_response(response)
            case _:
                return {"error": f"Action [{action}] is not supported"}
