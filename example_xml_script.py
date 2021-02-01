from xmldiff import main
from napalm import get_network_driver
driver = get_network_driver("sros")

optional_args = {"port": 830}

device = driver("127.0.0.1", "vagrant", "vagrant", 60, optional_args)

# opening the device
device.open()

# get the config of router
config = device.get_config()

# call load_replace with the config
device.load_replace_candidate(config=config["running"])

# get the candidate config
candidate_config = device.get_config(retrieve="candidate")

# compare candidate config to running config
result = main.diff_texts(config["running"], candidate_config["candidate"])

# commit the config
device.commit_config()

# closing device
device.close()
