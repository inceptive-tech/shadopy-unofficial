"""
    David G. - Inceptive - 2022
"""
from unittest import TestCase
from unittest.mock import patch

from shadopy import ShadowCloudCli, BlockDevices, BlockDevice
from shadopy.connexion import HttpBasicConnexion
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


@patch("requests.sessions.Session.send", side_effect=[ResMock(_BLOCK_LIST_TEST0)])
class TestShadowCloudCli(TestCase):
    def test_get_block_list_nominal(self, _):
        api = ShadowCloudCli(HttpBasicConnexion("test", "test"))
        result = api.get_block_list()
        expected = BlockDevices(block_devices=[BlockDevice(**_BLOCK_TEST0)])
        self.assertEqual(expected, result)
