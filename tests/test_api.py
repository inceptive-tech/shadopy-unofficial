"""
    David G. - Inceptive - 2022
"""
from unittest import TestCase
from unittest.mock import patch

from shadopy import ShadowCloudCli, BlockDevices, BlockDevice
from shadopy.connexion import HttpBasicConnexion
from shadopy.models import DataCenter, SkuInfo, UserInfo
from tests import ResMock

_BLOCK_TEST0 = {
    "id": 0,
    "uuid": "8d0f4962-0000-0000-0000-86bb7e6e4460",
    "status": 2,
    "status_str": "Allocated",
    "inserted_on": "2023-05-05T08:24:14.292Z",
    "affected_on": "2023-05-05T08:24:15.746Z",
    "allocated_on": "2023-05-05T08:24:16.555Z",
    "release_requested_on": None,
    "released_on": None,
    "mounted": False,
    "size_gib": 256,
    "cost": 4,
    "datacenter_label": "camtl01"
}
_BLOCK_LIST_TEST0 = {"block_devices": [_BLOCK_TEST0]}

_SKU_INFO_TEST0 = {
    "extra_core_cost": 15,
    "extra_gpu_cost": 50,
    "extra_ram_cost": 25,
    "hv_cpu_count": 2,
    "hv_cpu_ref": "2678v3",
    "hv_gpu_count": 4,
    "hv_gpu_ref": "p5000",
    "hv_ram": 64,
    "vm_core": 4,
    "vm_core_max": 16,
    "vm_cost": 100,
    "vm_gpu": 1,
    "vm_ram": 12,
    "vm_ram_max": 48,
    "vm_sku": "VM-P5000-2678V3-R2"
}
_USER_INFO_TEST0 = {
    "max_block_device": 1,
    "max_instances": 1,
    "max_request_timeout": 300,
    "superuser_level": 0,
    "vm_max_uptime": 5400
}
_CTX_TEST0 = {
    "datacenters": {
        "SK1": {
            "areas": [
                "South-Korea",
                "APAC"
            ],
            "label": "SK1"
        },
        "USSFO01": {
            "areas": [
                "North-America",
                "USA",
                "California"
            ],
            "label": "USSFO01"
        }
    },
    "user": _USER_INFO_TEST0,
    "vm": {
        "skus": {
            "VM-P5000-2678V3-R2": _SKU_INFO_TEST0,
            "VM-RTX4000-7513-R1": {
                "extra_core_cost": 23,
                "extra_gpu_cost": 78,
                "extra_ram_cost": 39,
                "hv_cpu_count": 1,
                "hv_cpu_ref": "7513",
                "hv_gpu_count": 8,
                "hv_gpu_ref": "rtx4000",
                "hv_ram": 128,
                "vm_core": 4,
                "vm_core_max": 32,
                "vm_cost": 155,
                "vm_gpu": 1,
                "vm_ram": 12,
                "vm_ram_max": 96,
                "vm_sku": "VM-RTX4000-7513-R1"
            }
        }
    }
}


class TestShadowCloudCli(TestCase):
    @patch("requests.sessions.Session.send", side_effect=[ResMock(_BLOCK_LIST_TEST0)])
    def test_get_block_list_nominal(self, _):
        api = ShadowCloudCli(HttpBasicConnexion("test", "test"))
        result = api.get_block_device_list()
        expected = BlockDevices(block_devices=[BlockDevice(**_BLOCK_TEST0)])
        self.assertEqual(expected, result)

    @patch("requests.sessions.Session.send", side_effect=[ResMock(_CTX_TEST0)])
    def test_get_ctx_info_nominal(self, _):
        api = ShadowCloudCli(HttpBasicConnexion("test", "test"))
        result = api.get_context_information()
        self.assertIn(DataCenter(label="SK1", areas=["South-Korea", "APAC"]), result.datacenters)
        self.assertIn(SkuInfo(**_SKU_INFO_TEST0), result.skus)
        self.assertEqual(UserInfo(**_USER_INFO_TEST0), result.user)

