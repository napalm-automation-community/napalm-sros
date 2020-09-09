## **Testing for NAPALM with Nokia SR OS**
1) To run the test framework, first install pytest: ```pip install pytest```
2) Locate the file: \"test/unit/sros/test_getters.py\" and run the class to test the getter methods
3) Locate the file \"test/unit/TestDriver.py\" and run \"Class TestConfigNokiaSROSDriver\" to test all the config methods of NAPALM
    + Location of files required by this test:
        - `napalm_sros/templates/set_hostname.j2`
        - `test/unit/sros/initial.conf` - Initial configuration sample
        - `test/unit/sros/merge_good.conf` - Merge config example
        - `test/unit/sros/merge_good.diff` - Compare output for merge
        - `test/unit/sros/merge_typo.conf` - Merege config example with error
        - `test/unit/sros/new_good.conf` - Replace config example
        - `test/unit/sros/new_good.diff` - Compare output for replace
        - `test/unit/sros/new_typo.conf` - Replace config example with error
4) Location of mocked output files used for these tests is : `test/unit/mocked_data`

We welcome suggestions and contributions of additional tests for the framework. Please contact the Nokia owners of this repository for how to contribute.
