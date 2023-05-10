"""
    Main API calls implementation
    David G. - Inceptive - 2023
"""
from typing import List
from urllib.parse import urljoin

from requests import Request, Session

from shadopy.connexion import BaseConnexion, HttpBasicConnexion
from shadopy.models import BlockDevices, ContextInformation, UserInfo, DataCenter, SkuInfo, VM, BlockDevice


class ShadowCloudCli:
    """wrapps the shadow cloud public APIs"""
    BASE_URL = "https://api.shdw-ws.fr"
    BLOCK_DEVICE_LIST_PATH = "/api/block_device/list"
    BLOCK_DEVICE_REQ_PATH = "/api/block_device/request"
    BLOCK_DEVICE_RELEASE_PATH = "/api/block_device/release"
    CTX_INFORMATION_PATH = "/api/context/informations"
    VM_LIST_PATH = "/api/vm/list"
    VM_REQ_PATH = "/api/vm/request"
    VM_KILL_PATH = "/api/vm/kill"

    ACCEPTED_BLOCK_DEVICES = [2 ** i for i in range(6, 12)]

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
        data = {} if block_uuid_filters is None else {"filters": [{"uuid": elt} for elt in block_uuid_filters]}
        serialized_blocks = self._build_and_send_request(self.BLOCK_DEVICE_LIST_PATH, data)
        return BlockDevices.parse_obj(serialized_blocks.json())

    def get_block_device(self, block_uuid: str) -> BlockDevice:
        # todo check lost size
        return self.get_block_device_list([block_uuid]).block_devices[0]

    def request_block_device(self, dc_label: str, size: int = None) -> BlockDevice:
        # TODO WIP
        assert size in self.ACCEPTED_BLOCK_DEVICES
        data = {"dry_run": False, "block_device": {"datacenter_label": dc_label}}
        if size is not None:
            data["block_device"]["size_gib"] = size
        serialized_block = self._build_and_send_request(self.BLOCK_DEVICE_REQ_PATH, data).json()
        return BlockDevice.parse_obj(serialized_block["block_device"])

    def release_block_device(self, block_device_uuid):
        data = {"block_device": {"uuid": block_device_uuid}}
        req_result = self._build_and_send_request(self.BLOCK_DEVICE_RELEASE_PATH, data)
        assert req_result.status_code == 200

    def get_context_information(self) -> ContextInformation:
        serialized = self._build_and_send_request(self.CTX_INFORMATION_PATH, {}).json()
        user = UserInfo.parse_obj(serialized["user"])
        datacenters = [DataCenter(**value) for _, value in serialized["datacenters"].items()]
        skus = [SkuInfo(**value) for _, value in serialized["vm"]["skus"].items()]
        return ContextInformation(datacenters=datacenters, user=user, skus=skus)

    def get_vm_list(self) -> List[VM]:
        # TODO WIP : add filters
        serialized = self._build_and_send_request(self.VM_LIST_PATH, {}).json()
        vms = [VM.parse_obj(elt) for elt in serialized["vms"]]
        return vms

    def request_vm(self, sku: str = None, image: str = None, pubkeys: List[str] = None,
                   core: int = None, ram: int = None, gpu: int = None, blocks: List[str] = None,
                   launch_script: str = None):
        data = {"dry_run": False, "vm": {}}
        if sku is not None:
            data["vm"]["sku"] = sku
        if image is not None:
            data["vm"]["image"] = image
        if pubkeys is not None:
            data["pubkeys"] = pubkeys
        if core is not None:
            data["vm"]["core"] = core
        if ram is not None:
            data["vm"]["ram"] = ram
        if gpu is not None:
            data["vm"]["gpu"] = ram
        if blocks is not None:
            data["vm"]["block_devices"] = [{"uuid": elt} for elt in blocks]
        if launch_script is not None:
            data["vm"]["launch_bash_script"] = launch_script
        resp = self._build_and_send_request(self.VM_REQ_PATH, data)
        assert resp.status_code == 200
        serialized = resp.json()
        return VM.parse_obj(serialized["vm"])

    def kill_vm(self, uuid: str):
        response = self._build_and_send_request(self.VM_KILL_PATH, {"dry_run": False, "vm": {"uuid": uuid}})
        assert response.status_code == 200
