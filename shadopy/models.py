"""
    input and output models of the shadow cloud API
    David G. - Inceptive - 2022
"""
from typing import Optional, List

from pydantic import BaseModel


class BlockDevice(BaseModel):
    allocated_on: Optional[str]
    cost: int
    datacenter_label: Optional[str]
    id: Optional[str]
    inserted_on: Optional[str]
    mounted: Optional[bool]  # named 'mount' in doc
    released_on: Optional[str]
    size_gib: int
    status: Optional[int]
    status_str: Optional[str]
    uuid: str


class BlockDevices(BaseModel):
    block_devices: List[BlockDevice]


class DataCenter(BaseModel):
    areas: List[str]
    label: str


class UserInfo(BaseModel):
    max_block_device: int
    max_instances: int
    max_request_timeout: int
    superuser_level: int
    vm_max_uptime: int


class SkuInfo(BaseModel):
    extra_core_cost: int
    extra_gpu_cost: int
    extra_ram_cost: int
    hv_cpu_count: int
    hv_cpu_ref: str
    hv_gpu_count: int
    hv_gpu_ref: str
    hv_ram: int
    vm_core: int
    vm_core_max: int
    vm_cost: int
    vm_gpu: int
    vm_ram: int
    vm_ram_max: int
    vm_sku: str


class ContextInformation(BaseModel):
    datacenters: List[DataCenter]
    user: UserInfo
    skus: List[SkuInfo]
