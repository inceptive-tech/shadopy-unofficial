"""
    input and output models of the shadow cloud API
    David G. - Inceptive - 2022
"""
from typing import Optional, List

from pydantic import BaseModel


class BlockDevice(BaseModel):
    allocated_on: str
    cost: int
    datacenter_label: str
    id: str
    inserted_on: str
    mounted: bool  # named 'mount' in doc
    released_on: Optional[str]
    size_gib: int
    status: int
    status_str: str
    uuid: str


class BlockDevices(BaseModel):
    block_devices: List[BlockDevice]


class DataCenter(BaseModel):
    name: str
    areas: List[str]
    label: str
