"""
    Wrapper around the auth systems of the shadow cloud API
    David G. - Inceptive - 2023
"""
import base64
import os

from requests import Request


class BaseConnexion:
    def prepare_req(self, req: Request):
        raise NotImplementedError()


class HttpBasicConnexion(BaseConnexion):

    def __init__(self, user: str = None, password: str = None) -> None:
        super().__init__()
        self._user = user if user is not None else os.environ["SPC_TEST_USER"]
        self._password = password if password is not None else os.environ["SPC_TEST_PASS"]
        self._token = base64.b64encode(f'{self._user}:{self._password}'.encode()).decode()

    def prepare_req(self, req: Request):
        req.headers["Authorization"] = f"Basic {self._token}"
        return req
