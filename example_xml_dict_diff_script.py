from napalm import get_network_driver

# import napalm driver and open the connection
driver = get_network_driver("sros")
optional_args = {"port": 830}
device = driver("127.0.0.1", "vagrant", "vagrant", 60, optional_args)

device.open()

# get the config in XML format
config = device.get_config()

# call load_replace
device.load_replace_candidate(filename="filename")

# get the candidate config in XML format
candidate_config = device.get_config(retrieve="candidate")

# xml diff between candidate and running
print(device.compare_config(running_config=config["running"], candidate_config=candidate_config["candidate"]))

# commit the config
device.commit_config()

# closing the device
device.close()
