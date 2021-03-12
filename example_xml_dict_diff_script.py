from napalm import get_network_driver

# import napalm driver and open the connection
driver = get_network_driver("sros")
optional_args = {"port": 830}
device = driver("138.120.181.55", "admin", "admin", 60, optional_args)
# device = driver("127.0.0.1", "vagrant", "vagrant", 60, optional_args)

device.open()

# call load_replace
device.load_replace_candidate(filename="config_1005_lines_new_180.xml")


# xml diff between candidate and running
print(device.compare_config())

# commit the config
device.commit_config()

# closing the device
device.close()
print("device closed")
