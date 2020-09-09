from napalm import get_network_driver

driver = get_network_driver("sros")
optional_args = {'port': 830}
device = driver("127.0.0.1", "vagrant", "vagrant", 60, optional_args)
device.open()
print(device.get_facts())
print(device.get_optics())
device.close()
