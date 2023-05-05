# shadopy-unofficial
Unofficial python cli for the Shadow cloud API: 
https://api.shdw-ws.fr/api/

Tested on python=3.10 - ubuntu 22.04
# Usage
```python
>>> from shadopy import ShadowCloudCli
>>> cli = ShadowCloudCli() # SPC_TEST_USER and SPC_TEST_PASS OS env. vars are used
>>> cli.get_context_information()
ContextInformation(datacenters=[DataCenter(areas=['Europe', 'Germany'], ...
>>> cli.get_block_device_list()
BlockDevices(block_devices=[BlockDevice(allocated_on='2023-05-05T08:07:24.989Z', ...

```
# TODOS

- [ ] /api/block_device/request
- [ ] /api/vm/request
  -  [ ] image == disk -> no ssh keys
- [ ] /api/block_device/release
- [ ] /api/vm/kill
- [ ] /api/vm/list
- [x] /api/block_device/list
- [x] /api/context/informations
- [ ] /api/context/availabilities
- [ ] /api/block_device/request
- [ ] error handling
- [ ] packaging
- [ ] pypi