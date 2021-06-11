from napalm import get_network_driver

# import napalm driver and open the connection
driver = get_network_driver("sros")
optional_args = {"port": 830}
device = driver("127.0.0.1", "vagrant", "vagrant", 60, optional_args)

device.open()

# call load_replace
device.load_replace_candidate(filename="filename")


# xml diff between candidate and running
print(device.compare_config())
# for json format use the below option
# print(device.compare_config(optional_args={'json_format':True}))

# commit the config
device.commit_config()

# closing the device
device.close()
print("device closed")
