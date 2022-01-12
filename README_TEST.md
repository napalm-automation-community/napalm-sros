## **Testing for NAPALM with Nokia SR OS**
1) To run the test framework, first install pytest: ```pip install pytest```
2) You can run the test two ways:
   1) Run command `python -m pytest`
   2) Locate and run the file `test/test_getters.py`

In order to run the tests using Docker and the minimal supported Python version:
```
docker run -it --rm --name run-test -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3.6 test/run_test.sh
```   

We welcome suggestions and contributions of additional tests for the framework. Please contact the Nokia owners of this repository for how to contribute.
