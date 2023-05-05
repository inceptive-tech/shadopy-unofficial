"""
    Main API calls implementation
    David G. - Inceptive - 2023
"""
from typing import List
from urllib.parse import urljoin

from requests import Request, Session

from shadopy.connexion import BaseConnexion, HttpBasicConnexion
from shadopy.models import BlockDevices, ContextInformation, UserInfo, DataCenter, SkuInfo


class ShadowCloudCli:
    """wrapps the shadow cloud public APIs"""
    BASE_URL = "https://api.shdw-ws.fr"
    BLOCK_DEVICE_LIST_PATH = "/api/block_device/list"
    CTX_INFORMATION_PATH = "/api/context/informations"

    def __init__(self, connexion: BaseConnexion = None) -> None:
        super().__init__()
        self.__connexion = connexion if connexion is not None else HttpBasicConnexion()

    def _build_and_send_request(self, uri_path, data: dict):
        """wrapps the POST API calls"""
        s = Session()
        url = urljoin(self.BASE_URL, uri_path)
        req = Request('POST', url, json=data)
        self.__connexion.prepare_req(req)
        prepped = req.prepare()
        return s.send(prepped)

    def get_block_device_list(self, block_uuid_filters: List[str] = None) -> BlockDevices:
        # todo use filters
        data = {} if block_uuid_filters is None else {"filters": [{"uuid": elt} for elt in block_uuid_filters]}
        serialized_blocks = self._build_and_send_request(self.BLOCK_DEVICE_LIST_PATH, data)
        return BlockDevices.parse_obj(serialized_blocks.json())

    def get_context_information(self) -> ContextInformation:
        serialized = self._build_and_send_request(self.CTX_INFORMATION_PATH, {}).json()
        user = UserInfo.parse_obj(serialized["user"])
        datacenters = [DataCenter(**value) for _, value in serialized["datacenters"].items()]
        skus = [SkuInfo(**value) for _, value in serialized["vm"]["skus"].items()]
        return ContextInformation(datacenters=datacenters, user=user, skus=skus)
