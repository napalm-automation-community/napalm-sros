## **Testing for NAPALM with Nokia SR OS**
1) To run the test framework, first install pytest: ```pip install pytest```
2) You can run the test two ways:
   1) Run command `python -m pytest`
   2) Locate and run the file `test/test_getters.py` 
   
Note: The test "test_get_interfaces" passes for CI/CD on Github, but it does not pass on individual local system due to 
computational difference on different Operating Systems of date and time.


We welcome suggestions and contributions of additional tests for the framework. Please contact the Nokia owners of this repository for how to contribute.
