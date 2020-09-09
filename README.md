## **NAPALM INTEGRATION WITH NOKIA SR OS**

#### **NAPALM**
NAPALM (Network Automation and Programmability Abstraction Layer with Multivendor support) is a Python library that implements a set of functions to interact with different router vendor devices using a unified API.

NAPALM supports several methods to connect to the devices, to manipulate configurations or to retrieve data.

#### **SR OS**
NAPALM integration is validated with a minimum of Nokia Service Router Operating System (SR OS) version 19.10R5. Releases beyond this have not been validated and should be by users before using the driver in labs and production on devices using different SR OS versions. Please contact the Nokia owners of this repository for additional information with respect to additional release validation.


#### **Documentation**
1) Please read the installation instruction in [Install Document](https://github.com/napalm-automation-community/napalm-sros/blob/master/Install.md)
2) The main files included for Nokia SR OS driver are:
     3) napalm_sros/sros.py: Overridden NAPALM methods to get the expected output from SR OS
     4) napalm_sros/nc_filters.py: Filters defined to get data from SR OS using a NETCONF connection
5) Mapping of various parameters of NAPALM output to Nokia SR OS can be found in this [Mapping Document](https://github.com/napalm-automation-community/napalm-sros/blob/master/Summary_of_Methods.pdf)
6) For testing, please refer to [Test Document](https://github.com/napalm-automation-community/napalm-sros/blob/master/README_TEST.md)

#### **Components Version**
1) Python - 3.6
2) ncclient >= 0.6.7
3) paramiko >= 2.7.1
4) NAPALM >= 3.0.1

##### **Note**
This version of the driver leverages Nokia’s defined YANG models for configuration and state trees for the SROS platform. While SROS also support limited configuration and state retrieval using openconfig standard models, the NAPALM driver does not support configuration or state retrieval of openconfig data models.

#### License
This project is licensed under the Apache-2.0 license - see the [LICENSE](LICENSE) file. 

