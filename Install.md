## Installation Steps

1) To enable NETCONF on SR OS, establish SSH connection with SR OS and follow the below steps:
    - Ensure model-driven is mode enabled
         ```
       A:vsim10# configure system management-interface configuration-mode model-driven
        ```
    - Enable NETCONF and NETCONF auto-save
        ```
        (gl)[configure system management-interface]
        A:admin@vsim10#
            netconf {
                admin-state enable
                auto-config-save true
            }
        ```
    - Select YANG models to use
        ```
        (gl)[configure system management-interface]
        A:admin@vsim10#
            yang-modules {
                base-r13-modules false
                nokia-modules false
                nokia-combined-modules true
            }
        ```
    - Select NETCONF user and permissions 
        ```
        (gl)[configure system security user-params]
        A:admin@vsim10#
            local-user {
                user "netconf" {
                    password "nokia"
                    access {
                        netconf true
                    }
                    console {
                        member ["administrative"]
                    }
                }
            }
        ```
    - Grant lock and kill permissions
        ```
        (gl)[configure system security aaa local-profiles profile "administrative"]
        A:admin@vsim10#
        netconf {
            base-op-authorization {
                kill-session true
                lock true
            }
        }
       ```   

2) From [NAPALM NOKIA REPO](https://github.com/napalm-automation-community/napalm-sros) clone the repository on your local computer
    ```
   git clone https://github.com/napalm-automation-community/napalm-sros
   ``` 
   
3) Install requirements using command `pip install -r requirements.txt` 
4) Run a script to get the results.
   ##### Usage Example
    ```
    from napalm import get_network_driver

    driver = get_network_driver("sros")

    device = driver(hostname, username, password, timeout, optional_args)
    device.open()
    device.get_facts()
    device.get_optics()
    device.close()
   ```
 

We welcome suggestions and contributions. Please contact the Nokia owners of this repository for how to contribute.

